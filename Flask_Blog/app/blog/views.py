import re
from sqlalchemy import and_, extract, or_
from flask import Blueprint, render_template, request

from .models import Post, Category, Tag


# 前两个为必填参数，蓝图名称和模块名称
# url_prefix='/blog' 指定了前缀路径
bp = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates', static_folder='static')


def index():
    """
    首页
    ---
    tags:
        - 首页接口
    description:
        - 显示站内信息
    responses:
        200:
            description: OK
            example: {'code': 1, 'message': OK}
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page=page, per_page=9, error_out=False)
    post_list = pagination.items

    import random
    imgs = ['https://gimg2.baidu.com/image_search/src=http%3A%2F%2Finews.gtimg.com%2Fnewsapp_bt%2F0%2F14297516724%2F641&refer=http%3A%2F%2Finews.gtimg.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1673502104&t=80b40881482c684b6b5cfd4570283d1c',
            'https://img2.baidu.com/it/u=2048195462,703560066&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=333',
            'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Flmg.jj20.com%2Fup%2Fallimg%2F1113%2F052420110515%2F200524110515-2-1200.jpg&refer=http%3A%2F%2Flmg.jj20.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1673502162&t=986f3242d469df7f19fe558a3dd19c29']

    for post in post_list:
        post.img = random.sample(imgs, 1)[0]
        # post.img = random.choice(imgs)
    return render_template('index.html', pagination=pagination, post_list=post_list)


@bp.route('/category/<int:cate_id>')
def cates(cate_id):
    """
    类别文章
    ---
    tags:
        - blog
    decription:
        - 显示属于该类别的文章文章列表
    parameters:
        - name: cate_id
          in: path
          description: 类别的id值
          required: true
          type: number
    responses:
        '200':
            description: 返回该类别的文章信息
            schema:
                type: string
        'default':
            description: Unexpected Error
    """
    cate = Category.query.get(cate_id)
    page = request.args.get('page', default=1, type=int)

    pagination = post_list = Post.query.filter(Post.category_id == cate_id).\
        paginate(page=page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('cate_list.html', cate=cate, post_list=post_list, pagination=pagination, cate_id=cate_id)


@bp.route('/category/<int:cate_id>/<int:post_id>')
def detail(cate_id, post_id):
    """
    文章详情
    ---
    tags:
        - blog
    description:
        - 显示文章详情
    parameters:
        - name: cate_id
          in: path
          description: 类别id
          required: true
          type: number
        - name: post_id
          in: path
          description: 文章id
          required: true
          type: number
    responses:
        '200':
            description: 返回文章详情信息
        'default':
            description: Unexpected Error
    """
    cate = Category.query.get(cate_id)
    post = Post.query.get_or_404(post_id)

    # post.tags中保存的是Tag对象，在html中显示标签时会显示 <Tag 'tag1'> ，而不是 'tag1'
    # 所以通过传递一个包含 tag.name 的列表，在html显示正确的标签名
    tag_list = []
    for tag in post.tags:
        tag_list.append(tag.name)

    # 上一篇
    prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
    # 下一篇
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()

    return render_template(
        'detail.html', cate=cate, post=post, prev_post=prev_post, next_post=next_post, tag_list=tag_list
    )


@bp.context_processor
def inject_archive():
    # 文章归档日期注入上下文
    posts = Post.query.order_by(-Post.add_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in posts])

    # 标签
    tags = Tag.query.all()
    for tag in tags:
        tag.style = ['is-success', 'is-danger', 'is-black', 'is-light', 'is-primary', 'is-link', 'is-info', 'is-warning']

    # 最新文章
    new_posts = posts.limit(2)

    return dict(dates=dates, tags=tags, new_posts=new_posts)


@bp.route('/category/<string:date>')
def archive(date):
    """
    时间内发布的文章列表
    ---
    tags:
        - blog
    description:
        - 时间内发布的文章列表
    parameters:
        - name: date
          in: path
          description: 要查询的时间，例：2022年12月
          required: true
          type: string
    responses:
        '200':
            description: 返回时间内发布的文章列表
        'default':
            description: Unexpected Error
    """
    regex = re.compile(r'\d{4}|\d{2}')
    dates = regex.findall(date)

    page = request.args.get('page', 1, type=int)

    # 根据年月获取数据
    archive_posts = Post.query.filter(
        and_(
            extract('year', Post.add_date) == int(dates[0]),
            extract('month', Post.add_date) == int(dates[1])
        )
    )

    pagination = archive_posts.paginate(page=page, per_page=10, error_out=False)
    post_list = pagination.items

    return render_template('archive.html', post_list=post_list, pagination=pagination, date=date)


@bp.route('/tags/<int:tag_id>')
def tags(tag_id):
    """
    标签
    ---
    tags:
        - blog
    description:
        - 标签详情
    parameters:
        - name: tag_id
          in: path
          description: 标签id
          required: true
          type: number
    responses:
        '200':
            description: 返回标签信息
        'default':
            description: Unexpected Error
    """
    # 标签页
    tag = Tag.query.get(tag_id)
    return render_template('tags.html', post_list=tag.post, tag=tag)


@bp.route('/search')
def search():
    """
    搜索框
    ---
    tags:
        - blog
    description:
        - 搜索
    parameters:
        - name: words
          in: query
          description: 关键字
          required: false
          type: string
    responses:
        '200':
            description: 返回搜索到的内容
        'default':
            description: Unexpected Error
    """
    words = request.args.get('words', '', type=str)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.title.like('%'+words+'%')).\
        paginate(page=page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('search.html', post_list=post_list, pagination=pagination, words=words)
