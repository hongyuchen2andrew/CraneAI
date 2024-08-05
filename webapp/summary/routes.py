from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user
from flask_login import current_user
from datetime import datetime, timedelta
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

from webapp import db
from webapp.summary import bp
from webapp.summary.forms import SmartSummaryForm
from webapp.summary.utils import summarization, list_summarization, tSNE, kmeans
from webapp.models import Summary_v2, Capture

@bp.route("/smart_summary", methods=["GET", "POST"])
def smart_summary():
    form = SmartSummaryForm()
    user_input = None
    if form.validate_on_submit():
        user_input = form.user_input.data
        length = form.length.data
        style = form.style.data
        time_range = form.time_range.data
        # 可以根据需要处理这些数据
        return redirect(url_for("summary.smart_summary_result", user_input=user_input, length=length, style=style, time_range=time_range))
    
    return render_template("summary/smart_summary.html", form=form, user_input=user_input)

@bp.route("/smart_summary_result")
def smart_summary_result():
    time_range = request.args.get('time_range', '')
    now = datetime.now()
    if time_range == '24h':
        time_gap = now - timedelta(hours=24)
    elif time_range == '3d':
        time_gap = now - timedelta(hours=24*3)
    elif time_range == '1w':
        time_gap = now - timedelta(hours=24*7)

    captures = Capture.query.filter(
        Capture.user_id == current_user.id,
        Capture.created_at >= time_gap
    ).with_entities(Capture.markdown_content, Capture.link, Capture.title, Capture.user_id).all()
    doc =[cap[0] for cap in captures]
    links =[cap[1] for cap in captures]
    titles =[cap[2] for cap in captures]
    print(11111111111111)
    print(titles)
    user_input = request.args.get('user_input', '')
    length = request.args.get('length', '')
    style = request.args.get('style', '')
    summary, summary_list = list_summarization(doc, user_input, length, style)
    for i in range(len(titles)):
        save_summary = Summary_v2(
            summary_title=titles[i],
            user_id=current_user.id,
            summary=summary,
            created_at=datetime.now(),
            embedding=[1,2,3,4],
        )
        db.session.add(save_summary)
        db.session.commit()
    #s = Summary_v2.query.filter_by(user_id=current_user.id).all()
    s = Summary_v2.query.with_entities(Summary_v2.created_at, Summary_v2.summary_title).all()
    print(123456789)
    print(s)
    # embeddings_2d = tSNE(summary_list)
    # clusters = kmeans(embeddings_2d)

    # fig, ax = plt.subplots()
    # scatter = ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=clusters, cmap='viridis')
    # legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    # ax.add_artist(legend1)
    # for i, txt in enumerate(summary_list):
    #     ax.annotate(f'Doc {i+1}', (embeddings_2d[i, 0], embeddings_2d[i, 1]))
    # ax.set_title('t-SNE Visualization of Document Clusters')

    # # 将图像保存到缓冲区并转换为Base64编码
    # buf = io.BytesIO()
    # fig.savefig(buf, format='png')
    # buf.seek(0)
    # image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    # buf.close()
   
    return render_template("summary/smart_summary_result.html", summary=summary, user_input=user_input, length=length, style=style, links=links)

