from project.app.scrapper import user_signin, parse_data, output_data
from project.app.update_README import write_tweets, update_readme
import time

if __name__ == "__main__":
    start = time.time()
    data = user_signin()
    tweets = parse_data(data)
    # output_data(tweets)
    end = time.time()

    write_tweets('recent_tweets.md', tweets)
    update_readme()
    print(end-start)
