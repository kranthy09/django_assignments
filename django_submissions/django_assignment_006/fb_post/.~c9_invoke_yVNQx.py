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
    
#-----------------------------------Task-12-------------------------------------------
  
def get_replies_for_comment(comment_id):
    
    comments = Comment.objects.filter(parent_comment_id=comme)