from krrishmahar.scrapper import user_signin, parse_data
from krrishmahar.update_README import write_tweets, update_readme

if __name__ == "__main__":
    data = user_signin()
    tweets = parse_data(data)

    write_tweets('recent_tweets.md', tweets)
    update_readme()