from flask import Blueprint, jsonify, make_response, request
from data import db_session
from data.jobs import Jobs

blueprint = Blueprint("jobs_api", __name__, template_folder="templates")


@blueprint.route("/api/jobs")
def get_jobs():
    sess = db_session.create_session()
    job_list = sess.query(Jobs).all()
    return jsonify({
        "jobs": [job.to_dict(only=("id", "job",
                                   "team_leader", "work_size",
                                   "collaborators", "start_date",
                                   "end_date", "is_finished")) for job in job_list]
    })


@blueprint.route("/api/jobs/<job_id:int>")
def get_jobs_id(job_id):
    sess = db_session.create_session()
    job_list = sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job_list:
        return make_response(jsonify({"status": "Not found"}, 404))
    return jsonify({
        "job": [job_list.to_dict(only=("id", "job",
                                       "team_leader", "work_size",
                                       "collaborators", "start_date",
                                       "end_date", "is_finished"))]
    })


@blueprint.route("/api/jobs", method=["POST"])
def create_jobs():
    if not request.json():
        return make_response(jsonify({"error": "Bad request"}), 400)

    column = ["id", "job", "team_leader", "work_size",
              "collaborators", "start_date",
              "end_date", "is_finished"]
    if all([key in column for key in request.json]):
        return make_response(jsonify({"error": "Bad request"}), 400)
    sess = db_session.create_session()
    jobs = Jobs()
    jobs.team_leader = request.json["team_leader"]
    jobs.job = request.json["job"]
    jobs.id = request.json["id"]
    jobs.work_size = request.json["work_size"]
    jobs.collaborators = request.json["collaborators"]
    jobs.start_date = request.json["start_date"]
    jobs.end_date = request.json["end_date"]
    jobs.is_finished = request.json["is_finished"]
    sess.add(jobs)
    sess.commit()
    return jsonify({"success": 200})
    