# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Question

def get_list_of_questions(request):
    list_of_questions = Question.objects.all()
    context = {
        "list_of_questions" : list_of_questions
    }
    
    return render(request, 'get_list_of_questions.html', context)

def create_question(request):
    if request.method == "GET":
        return render(request, 'create_question_form.html')
    elif request.method == "POST":
        request_data = request.POST
        question = request_data['question']
        answer = request_data['answer']
        if not question or not answer:
            return render(request, 'create_question_failure.html')
        else:
            question = Question(text=request_data['question'], answer=request_data['answer'])
            question.save()
            return render(request, 'create_question_success.html')

def get_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'each_question_form.html', {'question':question})
    
def update_question(request, question_id):
    update_request_body = request.POST
    update_question = update_request_body['question']
    update_answer = update_request_body['answer']
    if not update_question or not update_answer:
        return render(request, 'update_question_failure.html')
    else:
        question = Question.objects.get(pk=question_id)
        question.text = update_request_body['question']
        question.answer = update_request_body['answer']
        question.save()
        return render(request, 'update_question_success.html')
        
def delete_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return render(request, 'delete_question_failure.html')
    question.delete()
    return render(request, 'delete_question_success.html')
    