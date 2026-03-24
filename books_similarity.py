import pandas as pd

def books_similarity(df_catalog,similar,noauthor):
    
    # Get the row of the Book with the enter ID
    df_value_book = df_catalog.loc[df_catalog["Text#"] == similar,["Text#","Title","Subjects","Authors","Issued"]].values[0]

    # Extracting values from the row and storing them in a dictionary
    dict_book = {
        "id":df_value_book[0],
        "title":df_value_book[1],
        "subject":df_value_book[2].split(";"),
        "author":df_value_book[3],
        "issued":df_value_book[4]
    }

    # List for store all similar book in the catalog
    list_similar_books = []
            
    # Loop for get all similar book in the catalog
    for subject in dict_book["subject"]:
        
        # Per subject of given Book, retrieval of all book with the subject
        similar_books = df_catalog.loc[
            df_catalog["Subjects"].str.contains(subject, na=False),
            ["Text#","Title","Subjects","Authors","Issued"]].values
        
        # if book with subject : extracting values from the all books and storing them in a dictionary
        if similar_books.shape[0] > 0 :
            for book in similar_books :
                list_similar_books.append({
                    "id":book[0],
                    "title":book[1],
                    "subject":book[2].split(";"),
                    "author":book[3],
                    "issued":book[4]
                }) 


    # Clean list of all similar books : no duplicates, excluding the given book
    clean_list_similar_books = []
    clean_list_similar_books_title = []
    for book in list_similar_books :

        # Check if the book has already been verified and if is not the given book and not contain the same title
        if book["title"] not in clean_list_similar_books_title and book["id"] != similar and dict_book["title"] not in book["title"]:

            # If you want a list of similar book without book from the same author
            if noauthor :
                if dict_book["author"] not in book["author"] :
                    clean_list_similar_books.append(book)
                    clean_list_similar_books_title.append(book["title"])

            else : 
                clean_list_similar_books.append(book)
                clean_list_similar_books_title.append(book["title"])
    

    # Loop for count how many subject have a book with the given book
    for book in clean_list_similar_books :
        count = 0
        for subject in dict_book["subject"] :
            for book_subject in book["subject"]:
                if subject in book_subject :
                    count += 1
        book["subject_in_commun"] = count

    # Sort by the book with the most coummun subject with the given book
    sorted_clean_list_similar_books = sorted(clean_list_similar_books, key=lambda x: x["subject_in_commun"],reverse=True)

    # Loop for extract the top5 similar book and format data for dataframe
    dict_top5_similar_books = {"Id":[],"Title":[],"Category":[]}
    for i in range(5):
        dict_top5_similar_books["Id"].append(sorted_clean_list_similar_books[i]["id"])
        dict_top5_similar_books["Title"].append(sorted_clean_list_similar_books[i]["title"])
        dict_top5_similar_books["Category"].append(sorted_clean_list_similar_books[i]["subject"])


    df_top5_similar_books = pd.DataFrame(dict_top5_similar_books)
    
    # If you want a file for see all similar book
    # with open("sorted_clean_list_similar_books.json", "w") as file:
    #     json.dump(sorted_clean_list_similar_books, file, indent=4)

    return df_top5_similar_books
        