from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app.forms.team import TeamForm

