from .decorator import profile

@profile()
def my_function():
    import time
    time.sleep(2)
    print("Exiting my function")
    
@profile()
def get_books_by_library_id_one_query(book_ids):
    from db_optimization.models import Book
    from collections import defaultdict
    books = Book.objects.filter(id__in=book_ids)
    result = defaultdict(list)
    
    for book in books:
        result[book.library_id].append(book)
    return result
    
@profile()
def get_books_by_library_id(book_ids):
    from db_optimization.models import Book
    from collections import defaultdict
    result = defaultdict(list)
   
    for book_id in book_ids:
        book = Book.objects.get(id=book_id)
        result[book.library_id].append(book)
    return result

@profile()
def get_books_by_author():
    from db_optimization.models import Book         
    from collections import defaultdict    
    books = Book.objects.all()[:30]
    result = defaultdict(list)
    for book in books:
        author = book.author
        title_and_author = '{} by {}'.format(
            book.title,
            author.name
        )
        result[book.library_id].append(title_and_author)
    return result

@profile()
def get_books_by_author_select_related():
    from db_optimization.models import Book
    from collections import defaultdict
    books = Book.objects.all().select_related('author')[:30]
    result = defaultdict(list)
    for book in books:
        author = book.author
        title_and_author = '{} by {}'.format(
            book.title,
            author.name
        )
        result[book.library_id].append(title_and_author)
    return result