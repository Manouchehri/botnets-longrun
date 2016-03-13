#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, abort, request, jsonify, g, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import celery
import keyworder
import images
import json
from celery import Celery

# init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['CELERY_BROKER_URL'] = 'sqla+sqlite:///celerydb.sqlite'

# celery
celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    backend='db+sqlite:///results.sqlite',
)
celery.conf.update(app.config)

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201)


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@app.route('/api/users/<username>')
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

@celery.task
def celery_test_task(word):
    return "Hello: %s" % word


@app.route('/api/celerytest')
def celery_test():
    # Partir la task...
    task_id = celery_test_task.delay("world").task_id
    # Fetch le résultat
    result = celery_test_task.AsyncResult(task_id)
    # Biensur l'idée c'est pas de faire ca de facon synchrone, mais ceci
    # démontre l'utilisation de celery...
    return "Task result: %s" % result.get()

@app.route('/')
def serve_root():
    return redirect('/static/index.html')

@celery.task
def task_get_images(keyword):
    return images.get_images(keyword)

@app.route('/api/images', methods=['POST'])
@auth.login_required
def get_images():
    text = request.form['text']

    # Using celery to start multiple tasks to retrieve images
    keywords = keyworder.get_keywords(text)
    tasks = []
    for keyword in keywords:
        task_id = task_get_images.delay(keyword).task_id
        tasks.append(task_id)

    # Now get the result of all tasks
    imgs = []
    for task_id in tasks:
        result = task_get_images.AsyncResult(task_id).get()
        imgs.append(result)

    return json.dumps(imgs)



if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()

        # Create test user
        user = User(username='admin')
        user.hash_password('admin')
        db.session.add(user)
        db.session.commit()

    app.run(debug=True)
