from flask import request, abort, redirect, make_response
from flask_cors import cross_origin
from ...config import AppConfig
from ...lib.flask.decorator import json_content_type
from ...lib.flask.response import response
from ...service.sso.auth import ServiceSSOAuth
from .. import sso_blueprint
from ._auth import auth as _auth


cookie_config = AppConfig().flask["cookie-config"]


@sso_blueprint.route("/", methods=["GET"])
@cross_origin()
def index():
    if not (_redirect:=request.args.get("redirect", "") or request.headers.get("Referer", "")):
        abort(401)
    params = f"{'&' if '?' in _redirect else '?'}{cookie_config['key']}={hash_account}" if (hash_account:=request.cookies.get(cookie_config["key"])) and ServiceSSOAuth().get_user_with_hash_account(hash_account) else ""
    return redirect(_redirect + params)


@sso_blueprint.route("/auth", methods=["GET", "POST"])
@cross_origin()
@json_content_type()
def auth():
    rsp = {
        "code": 500,
        "msg": "服务器出现未知错误，请联系管理员！"
    }
    if not (hash_account:=request.args.get(cookie_config["key"]) if request.method == "GET" else request.get_json().get(cookie_config["key"])):
        abort(400)
    if user:=ServiceSSOAuth().get_user_with_hash_account(hash_account):
        rsp["code"] = 200
        rsp["msg"] = "用户认证成功！"
    else:
        rsp["code"] = 400
        rsp["msg"] = "用户认证失败！"
    rsp["data"] = user
    return response(**rsp)


@sso_blueprint.route("/auth/login", methods=["GET"])
@cross_origin()
@json_content_type()
def auth_login():
    if not (_redirect:=request.args.get("redirect", "") or request.headers.get("Referer", "")):
        abort(401)
    params = f"{'&' if '?' in _redirect else '?'}{cookie_config['key']}={hash_account}" if (account:=request.args.get("account")) and (password:=request.args.get("password")) and (hash_account:=ServiceSSOAuth().sso_auth(account, password)) else ""
    rsp = make_response(redirect(_redirect + params))
    if hash_account:
        rsp.set_cookie(value=hash_account, **cookie_config)
    return rsp


@sso_blueprint.route("/auth/account", methods=["GET", "POST"])
@cross_origin()
@json_content_type()
def auth_account():
    rsp = {
        "code": 500,
        "msg": "服务器出现未知错误，请联系管理员！"
    }
    if request.method == "GET":
        account = request.args.get("account")
        password = request.args.get("password")
    else:
        data = request.get_json()
        account = data.get("account")
        password = data.get("password")
    if not (account and password):
        abort(400)
    if hash_account:=ServiceSSOAuth().sso_auth(account, password):
        rsp["code"] = 200
        rsp["msg"] = f"获取用户{cookie_config['key']}成功！"
        rsp["data"] = hash_account
    else:
        rsp["code"] = 400
        rsp["msg"] = f"获取用户{cookie_config['key']}失败！"
    return response(**rsp)


@sso_blueprint.route("/login", methods=["GET", "POST"])
@cross_origin()
@_auth
@json_content_type()
def login():
    rsp = {
        "code": 500,
        "msg": "服务器出现未知错误，请联系管理员！"
    }
    if not (hash_account:=request.args.get(cookie_config["key"]) if request.method == "GET" else request.get_json().get(cookie_config["key"])):
        abort(400)
    if (service_sso_auth:=ServiceSSOAuth()) and (user:=service_sso_auth.get_user_with_hash_account(hash_account)):
        if service_sso_auth.active_hash_account_to_all_project(hash_account, user):
            rsp["code"] = 202
            rsp["msg"] = "已激活！"
    else:
        rsp["code"] = 204
        rsp["msg"] = "哈希账号不存在或已失效！"
    return response(**rsp)


@sso_blueprint.route("/logout", methods=["GET", "POST"])
@cross_origin()
@_auth
@json_content_type()
def logout():
    rsp = {
        "code": 500,
        "msg": "服务器出现未知错误，请联系管理员！"
    }
    if not (hash_account:=request.args.get(cookie_config["key"]) if request.method == "GET" else request.get_json().get(cookie_config["key"])):
        abort(400)
    if ServiceSSOAuth().logout_hash_account_to_all_project(hash_account):
        rsp["code"] = 202
        rsp["msg"] = "已注销！"
    return response(**rsp)

