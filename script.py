from tokens import tokens
import requests
import random
from bs4 import BeautifulSoup
from PIL import Image
from resizeimage import resizeimage
from twython import Twython
import os

BASE_URL = 'https://en.wikipedia.org'
GET_RANDOM = '/wiki/Special:Random'

exceptions = [
    ',',
    'List',
    'list',
    'and',
    'refer',
    'these',
    'things',
    'or',
]
adjectives = [
    'weak',
    'loser',
    'lousy',
    'third-rate',
    'clueless',
    'failing',
    'overrated',
]
insults = [
    'is ruining this country.',
    'has destroyed our great nation.',
    'is clueless. Might be dangerous?',
    'is so average in every way.',
    'is killing us with political correctness.',
    'is very hostile toward me.',
    'had a failed career.',
    'is a failure and in total freefall.',
    'has no common sense.',
    'is such a total failure.',
    'is stealing our jobs - and Obama doesn\'t care!',
    'is TERRIBLE for America!',
    'has failed miserably.',
    'is a terrible, terrible thing.',
    'can\'t make AMERICA GREAT like I can.',
    'has got a lot of problems.',
    'has problems. Many respected people say so.',
    'has many, many problems.',
    'is a total lightweight.',
    'is a flunkie and a real dummy.',
    'just doesn\'t have a clue.',
    'is really boring.',
    'has been so wrong & is bad for our country.',
    'has no talent (and is boring)',
    'is very dishonest, a total liar.',
    'is total garbage.',
    'is such a hypocrite.',
    'is dumber than a rock.',
    'did very badly. The worst of all time?',
    'just doesn\'t have it. I alone can solve.',
    'has zero cred.',
    'has no credibility.',
    'failed us very badly.',
    'is so biased against me.',
    'did such a horrible job.',
    'is... I shouldn\'t say it, but... is a pussy.',
    'is such a joke and a total loser.',
    'is completely wrong & cannot be trusted.',
    'could be backed by ISIS? Many people say so.',
    'never wins at anything.',
    'is such a major sleaze.',
    'is making us very, very weak.',
    'is RUINING our nation like I predicted.',
    'is not good, not at all.',
    'has killed us with incompetence.',
    'is killing us! It\'s terrible.',
    'needs to be stopped, but weak Washington won\'t act.',
    'is totally killing us.',
    'is killing us, folks.',
    'is doing many bad things.',
    'is very unethical, folks.',
    'doesn\'t know how to win.',
    'is a total low life.',
    'will NEVER Make America Great Again.',
    'is very uncomfortable.',
    'is all talk no action.',
    'is very dishonest - a total fraud.',
    'is just hopeless.',
    'is one of the worst of all time.',
    'is a major hater.',
    'is, frankly, a total hater.',
    'is a HATER & a LOSER.',
    'is a hater (and very boring).',
    'is such a hater.',
    'is a total hater.',
    'is a major lightweight.',
    'should be forced to take an IQ test.',
    'knows nothing about business.',
    'is a total wacko.',
    'let us all down very badly.',
    'is even dumber than we thought.',
    'is very boring.',
    'has a horrible attitude.',
    'is terrible (and very boring).',
    'is a fool and not trusted by anyone.',
    'is totally irrelevant.',
    'is a real nut job.',
    'is a complete basketcase.',
    'does nothing but attack me.',
    'has issues. Many respected people think so.',
    'has a lot of issues, folks.',
    'deserves to be FIRED immediately.',
    'is absolutely disgraceful.',
    'is totally out of control.',
    'is broken, just like our country.',
    'is terrible (and boring).',
    'is so ridiculous.',
    'has no guts, no glory.',
    'gets terrible ratings.',
    'is poorly rated - a total disaster.',
    'is very boring & lame.',
    'is ripping us off. It\'s an outrage.',
    'is deeply troubled.',
    'is totally corrupt.',
    'is a horrow show like I predicted - but nobody listened.',
    'is KILLING us.',
    'has totally killed us.',
    'is not our friend.',
    'is corrupt. So corrupt, folks.',
    'is a total mess but refuses to fix anything.',
    'is small and unimportant.',
    'is so wrong, so often.',
    'is horrible and a complete mess.',
    'might be controlled by China?',
    'is giving away our money to CHINA, folks.',
    'is so dishonest & biased.',
    'is just killing us! We don\'t win anymore.',
    'is a puppet of the politicians.',
    'is considered by many to be the worst.',
    'is very incompetent. Many respected people agree.',
    'is totally worthless and an awful leader.',
    'is highly unethical and corrupt.',
    'isn\'t very bright.',
    'is in total turmoil. I predicted this.',
    'is killing us very badly.',
    'is so off, very crazy! Can\'t be trusted.',
    'is a troublemaker. Could be backed by ISIS?',
    'is a money-losing failure.',
    'has no $$ and has no talent.',
    'is not very good or professional.',
    'is so biased it is disgusting.',
    'is very dumb. Could have mental problems?',
    'can\'t get anything right.',
    'is so crazy & has no clue.',
    'is totally ineffective & has been for years.',
    'is very stupid & highly incompetent.',
    'is running the U.S.A. into the ground.',
    'is such a major phony.',
    'is killing us - killing our great nation.',
    'is majorly beating us.',
    'is a tool of ISIS! Many people say that.',
    'is very soft! No strength at all.',
    'is a major disgrace.',
    'has a major inferiority complex.',
    'is a dopey clown.',
    'is wrong on so many subjects.',
]
endings = [
    'SAD',
    'WOW',
    'Unbelieveable',
    'So sad',
    'Very sad',
    'Shameful',
    'Awful',
    'What a joke',
    'Disgusting',
    'How pathetic',
]


def get_tokens():
    app_key = tokens['app_key']
    app_secret = tokens['app_secret']
    oauth_token = tokens['oauth_token']
    oauth_token_secret = tokens['oauth_token_secret']
    return Twython(app_key, app_secret, oauth_token, oauth_token_secret)


def get_page(url_ending):
    return BeautifulSoup(requests.get(BASE_URL + url_ending).content, 'lxml')


def get_title(scraped_page):
    title = scraped_page.find(id='firstHeading')
    if title:
        title = title.get_text()
        if any(char in title for char in exceptions):
            return False
        else:
            return title


def get_image(scraped_page):
    image_link = scraped_page.find('a', class_='image')
    if image_link:
        image = image_link.find('img')
        if image and image.has_attr('data-file-width') and check_size(image):
            image_url = get_page(image_link['href']).find('a', class_='internal')['href']
            if image_type_correct(image_url):
                return image_url


def check_size(image):
    if int(image['data-file-width']) > 400:
        return True


def image_type_correct(image_url):
    if image_url.lower().endswith(('.png', '.jpg', '.jpeg')):
        return True


def save_image(image_url):
    image_name = image_url.split('/')[-1]
    f = open('img/' + image_name, 'wb')
    f.write(requests.get('http:' + image_url).content)
    f.close()
    image = 'img/' + image_name
    if os.path.getsize(image) > 3000000:
        resize_image(image)
    return image


def resize_image(image):
    f = open(image, 'r')
    img = Image.open(f)
    img = resizeimage.resize_width(img, 1000)
    img.save(image, img.format)
    f.close()


def fits_in_tweet(text):
    if len(text) > 116:
        return False
    else:
        return True


def write_tweet(title):
    if any(char.isdigit() for char in title):
        text = "Does anyone really think %s was any good? %s!" % (title, random.choice(endings))
    else:
        text = "The %s %s %s %s!" % (random.choice(adjectives), title, random.choice(insults), random.choice(endings))
    if fits_in_tweet(text):
        return text


def post_tweet(text, image):
    twitter = get_tokens()
    photo = open(image, 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status=text, media_ids=[response['media_id']])
    print text


def main():
    page = get_page(GET_RANDOM)
    title = get_title(page)
    image = get_image(page)
    if title and image:
        text = write_tweet(title)
        image_path = save_image(image)
        post_tweet(text, image_path)
    else:
        main()


if __name__ == '__main__':
    main()
