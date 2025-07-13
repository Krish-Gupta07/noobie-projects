import news_service
import summarizer
import bias_classifier


def main():
    while True:
        print("Welcome to the CLI News, how can i help you today?")
        print("Press 1 to get top headlines")
        print("Press 2 to get news about a topic")
        print("Press 3 to get breaking headlines")
        print("Press 4 to summarize the news article with AI")
        print("Press 5 to check for biasedness")
        
        try:
            choice = int(input("Type your choice: "))
        except ValueError:
            print("Please enter a valid number!\n")
            continue

        match choice:
            case 1:
                news_service.top_headlines()

            case 2:
                news_service.get_news()
            
            case 3:
                news_service.breaking_headlines()

            case 4:
                summarizer.summarize_news()

            case 5:
                bias_classifier.bias_check()
            
            case 0:
                print("See you later alligator")
                break
            
            case _:
                print("Invalid option. Try again. \n")



    

if __name__ == "__main__":
    main()
