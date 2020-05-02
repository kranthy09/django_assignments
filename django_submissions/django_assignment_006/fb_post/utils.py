from .models import Post, User, Comment, Reaction
from .exceptions import InvalidPostContent, InvalidUserException,InvalidPostException, InvalidCommentContent, InvalidCommentException, InvalidReplyContent, InvalidReactionTypeException, UserCannotDeletePostException
from .constants import ReactionChoice
from django.db.models import Count, Prefetch

#------------------------------exception_fucntions-----------------------------------

def check_is_valid_user_id(user_id):
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException
    
    return user


def check_is_valid_post_content(post_content):
    
    if not post_content:
        raise InvalidPostContent
    
    return

def check_is_valid_comment_content(comment_content):
    
    if not comment_content:
        raise InvalidCommentContent
    
    return
    
def check_is_valid_post_id(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise InvalidPostException
    
    return post

def check_is_valid_comment_id(comment_id):
    
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise InvalidCommentException
    
    return comment

def check_is_valid_reply_content(reply_content):
    
    if not reply_content:
        
        raise InvalidReplyContent
    
    return

def check_is_valid_reaction_type(reaction_type):
    
    if reaction_type not in ReactionChoice.values:
        
        raise InvalidReactionTypeException
    
    return

def check_is_user_is_creator_of_post(user_id, post_id):
    
    post_object = Post.objects.get(id = post_id)
    
    is_both_user_id_are_same = post_object.posted_by.id == user_id
    
    if not is_both_user_id_are_same:
        raise UserCannotDeletePostException
    
    return

def create_user(name,profile_pic):
    user = User.objects.create(name=name, profile_pic=profile_pic)
    return user.id
#-----------------------------------Task-2-------------------------------------------

def create_post(user_id, post_content):
    user = check_is_valid_user_id(user_id)
    check_is_valid_post_content(post_content)

    post = Post.objects.create(content=post_content, posted_by=user)
    
    return post.id

#-----------------------------------Task-3-------------------------------------------

def create_comment(user_id, post_id, comment_content):
    
    user = check_is_valid_user_id(user_id)
    post = check_is_valid_post_id(post_id)
    check_is_valid_comment_content(comment_content)
    
    comment = Comment.objects.create(commented_by=user, post=post, content=comment_content)
    
    return comment.id
    
#-----------------------------------Task-4-------------------------------------------

def reply_to_comment(user_id, comment_id, reply_content):
    
    user = check_is_valid_user_id(user_id)
    comment = check_is_valid_comment_id(comment_id)
    check_is_valid_reply_content(reply_content)
    
    post_id_parent_comment = comment.post
    comment = Comment.objects.create(content=reply_content, 
                                     commented_by=user,
                                     parent_comment=comment, 
                                     post=post_id_parent_comment
                                    )

#-----------------------------------Task-5-------------------------------------------

def react_to_post(user_id, post_id, reaction_type):
    
    user = check_is_valid_user_id(user_id)
    post = check_is_valid_post_id(post_id)
    check_is_valid_reaction_type(reaction_type)
    
    try:
        reaction_object = Reaction.objects.get(reacted_by_id=user_id, post_id=post_id)
    except Reaction.DoesNotExist:
        Reaction.objects.create(post = post, reaction=reaction_type, reacted_by=user)
        return
    
    is_both_reactions_are_same = reaction_object.reaction == reaction_type
    
    if is_both_reactions_are_same:
            reaction_object.delete()
    else:
        reaction_object.reaction = reaction_type
        reaction_object.save()
        
    return

#-----------------------------------Task-6-------------------------------------------

def react_to_comment(user_id, comment_id, reaction_type):
    
    user = check_is_valid_user_id(user_id)
    comment = check_is_valid_comment_id(comment_id)
    check_is_valid_reaction_type(reaction_type)
    
    try: 
        reaction_object = Reaction.objects.get(reacted_by_id=user_id, comment_id=comment_id)
        
    except Reaction.DoesNotExist:
        Reaction.objects.create(reacted_by_id=user_id, comment_id=comment_id, reaction=reaction_type)
        return
    
    is_both_reactions_are_same = reaction_object.reaction == reaction_type
    
    if is_both_reactions_are_same:
            reaction_object.delete()
    else:
        reaction_object.reaction = reaction_type
        reaction_object.save()
    
    return

#-----------------------------------Task-7-------------------------------------------

def get_total_reaction_count():
    
    total_reaction_count = Reaction.objects.aggregate(count=Count('reaction'))
    
    return total_reaction_count

#-----------------------------------Task-8-------------------------------------------

def get_reaction_metrics(post_id):
    
    check_is_valid_post_id(post_id)
    
    reaction_metrics = Reaction.objects.filter(post_id=post_id).values_list('reaction').annotate(count=Count('reaction'))
    
    
    return dict(reaction_metrics)
    
#-----------------------------------Task-9-------------------------------------------

def delete_post(user_id, post_id):
    
    check_is_valid_user_id(user_id)
    check_is_valid_post_id(post_id)
    check_is_user_is_creator_of_post(user_id, post_id)
    
    Post.objects.filter(id=post_id).delete()
    
    return

#-----------------------------------Task-10-------------------------------------------

def get_posts_with_more_positive_reactions():
    
    posts = Post.objects.prefetch_related(Prefetch('reaction_set', to_attr='reactions_to_this_post'))
    posts_list = []
    positive_reactions = ['THUMBS-UP', 'LIT', 'LOVE', 'HAHA', 'WOW']
    
    for post in posts:
        count_positive_reactions = 0
        count_negative_reactions = 0
        for reaction_object in post.reactions_to_this_post:
            if reaction_object.reaction in positive_reactions:
                count_positive_reactions += 1
            else:
                count_negative_reactions += 1
        
        if count_positive_reactions > count_negative_reactions:
            posts_list.append(post.id)
    
    return posts_list
    
#-----------------------------------Task-11-------------------------------------------

def get_posts_reacted_by_user(user_id):
    
    check_is_valid_user_id(user_id)
    post_ids = list(Reaction.objects.filter(reacted_by=user_id, post_id__isnull=False).values_list('post_id', flat=True))
    
    return post_ids
    
#-----------------------------------Task-12-------------------------------------------

def get_reactions_to_post(post_id):
    
    check_is_valid_post_id(post_id)
    
    reaction_objects = Reaction.objects.filter(post_id=post_id).select_related('reacted_by')
    reactions_of_post_list = []
    for reaction_obj in reaction_objects:
        
        reactions_of_post_list.append(
                        {
                            "user_id" : reaction_obj.reacted_by.id,
                            "name" : reaction_obj.reacted_by.name,
                            "profile_pic" : reaction_obj.reacted_by.profile_pic,
                            "reaction" : reaction_obj.reaction
                        }
                    )
    
    return reactions_of_post_list

#-----------------------------------Task-13-------------------------------------------

def replies_to_the_parent_comment(parent_comment, comments_list):
    replies_list = []
    for comment in comments_list:
        if comment.parent_comment == parent_comment:
            replies_list.append(comment)
    
    return replies_list

def get_post(post_id):
    
    queryset = Comment.objects.select_related('commented_by').prefetch_related(Prefetch('reaction_set', to_attr='reactions'))
    
    post = Post.objects.filter(post_id=post_id).select_related('posted_by').prefetch_related(Prefetch('reaction_set', to_attr='reactions'), Prefetch('comment_set', queryset=queryset, to_attr='comments'))
    
    query_dict = {}
    comments_list = []
    query_dict['post_id'] = post.id
    query_dict['posted_by'] =  {
        "name" : post.posted_by.name,
        'user_id' : post.posted_by.id,
        'profile_pic' : post.posted_by.profile_pic
    }
    query_dict['posted_at'] = post.posted_at
    query_dict['post_content'] = post.post_content
    query_dict['reactions'] = {
        "count" : len(post.reactions),
        "type" : [reaction_obj.reaction for reaction_obj in post.reactions]
    }
    query_dict['comments'] = comments_list
    comments = post.comments
    if comments:
        comments_list = []
    else:
        comment_dict = {}
        parent_comments_list = []
        for comment in comments:
            if not comment.parent_comment:
                comment.parent_comments_list
        for parent_comment in parent_comments_list:
            
            replies = replies_to_the_parent_comment(parent_comment, comments)
            comment_dict['comment_id'] = parent_comment.id
            comment_dict['comment_content'] = parent_comment.content
            comment_dict['reactions'] = {
                "count" : len(parent_comment.reactions),
                "type" : [reaction_obj.reaction for reaction_obj in parent_comment.reactions]
            }
            comment_dict['replies_count'] : len(replies)
            comment_dict['replies'] : replies
            if replies:
                replies = []
            else:
                reply_dict = {}
                for reply in replies:
                    reply_dict['comment_id'] = reply.id
                    reply_dict['commenter'] = {
                        'user_id' : reply.commented_by.id,
                        'name' : reply.commented_by.name,
                        'profile_pic' : reply.commented_by.profile_pic
                    }
                    reply_dict['commented_at'] : reply.commented_at
                    reply_dict['comment_content'] : reply.content
                    reply['reactions'] = {
                        "count" : len(reply.reactions),
                        "type" : [reaction_obj.reaction for reaction_obj in reply.reactions]
                    }
                replies.append(reply_dict)
            
            #have to check about the comments_list
            
    return
    
#-----------------------------------Task-15-------------------------------------------
  
def get_replies_for_comment(comment_id):
    
    comments = Comment.objects.filter(parent_comment_id=comment_id).select_related('commented_by')
    
    replies_for_comment_list = []
    
    for comment in comments:
        
        replies_for_comment_list.append(
                {
            "comment_id": comment.id,
            "commenter": {
                    "user_id": comment.commented_by.id,
                    "name": comment.commented_by.name, 
                    "profile_pic": comment.commented_by.profile_pic
                },
            "commented_at": comment.commented_at,
            "comment_content": comment.content,
        }
                )
    
    return replies_for_comment_list