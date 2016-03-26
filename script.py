import requests
import random
from bs4 import BeautifulSoup
from tokens import tokens
from twython import Twython
import time


BASE_URL = 'https://en.wikipedia.org'
RANDOM = '/wiki/Special:Random'

exceptions = [
    '(',
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
    'pathetic',
    'loser',
    'lousy',
    'third-rate',
    'LOSER',
    'dumb',
    'clueless',
    'failing',
    'overrated',
]
insults = [
    'is ruining the country we love',
    'has destroyed our great nation',
    'is clueless',
    'is so average in every way',
    'is very politically correct',
    'is very hostile, folks',
    'had a failed career',
    'is a cheater',
    'is in total freefall',
    'has no common sense',
    'is such a total failure to us all',
    'was terrible',
    'is stealing our jobs',
    'is TERRIBLE for America',
    'has failed miserably',
    'has done nothing. I\'m no fan'
    'is just a terrible, terrible thing',
    'can\'t make AMERICA GREAT like I can',
    'has got a lot of problems',
    'has problems - many of them',
    'has a lot of problems',
    'is such a dope',
    'is a total lightweight',
    'is a flunkie and a real dummy',
    'is not a leader! Such a disaster',
    'just doesn\'t have a clue',
    'is really boring',
    'has been so wrong & is bad',
    'has no talent',
    'has no talent (& is boring)',
    'is very dishonest',
    'is total garbage',
    'is such a hypocrite',
    'is the WORST EVER',
    'has never won at anything',
    'won\'t apologize to me',
    'better hope I don\'t sue! I WILL win',
    'is dumber than a rock',
    'did very badly',
    'just doesn\'t have IT',
    'has zero cred',
    'has no credibility',
    'failed us very badly',
    'is a sad sack (and boring)',
    'is too soft to be a leader',
    'is so biased against me',
    'should be ashamed',
    'did such a horrible job',
    'can\'t be trusted',
    'is desperate for attention',
    'is... I shouldn\'t say it... is a pussy',
    'has no imagination',
    'is such a joke. A total loser',
    'is completely wrong',
    'might be backed by ISIS',
    'never wins at anything, folks',
    'is very bad',
    'is such a major sleaze',
    'is making us very, very weak',
    'is RUINING our nation, folks',
    'is not good',
    'is killing us',
    'is killing us! It\'s very bad',
    'is doing many bad things',
    'is very unethical, folks',
    'just doesn\'t know how to win',
    'should be fired like a DOG',
    'is a total low life',
    'will NEVER Make America Great Again',
    'is very uncomfortable',
    'is all talk no action',
    'is very dishonest - a FRAUD',
    'knows nothing',
    'will be fired like a dog',
    'is just hopeless',
    'is so easy to beat',
    'is one of the worst in history',
    'is wasting time & money',
    'is truly weird',
    'is a zero',
    'is a hater',
    'is a major hater',
    'is a HATER',
    'is a hater (and very boring)',
    'is such a hater',
    'is a total hater',
    'is a hater & a racist',
    'has no fans',
    'did really poorly on television',
    'is a major lightweight',
    'should be forced to take an IQ test',
    'needs to give up',
    'has the worst record',
    'treats America like trash',
    'is just another failure',
    'is not as smart as me',
    'knows nothing about business',
    'is a WACKO',
    'is a sicko',
    'let us down very badly',
    'is even dumber than we thought',
    'is very boring',
    'has a horrible attitude',
    'is terrible (and very boring)',
    'is a fool',
    'did a terrible job, folks',
    'is irrelevant',
    'is a real nut job',
    'is a real basketcase',
    'has weird issues. Mental issues',
    'is wacky',
    'deserves to be FIRED',
    'is not nice',
    '-- what a joke! A real phony, folks',
    'is absolutely disgraceful',
    'is totally out of control',
    'is broken, just like our country',
    'is terrible (and boring)',
    'is very boring',
    'is weak (and looks strange)',
    'is so ridiculous',
    'has no guts, no glory',
    'is very bad for U.S.A',
    'is poorly rated - a total disaster',
    'doesn\'t get the ratings I do',
    'is very boring & lame',
    'is an outrage',
    'has never made a profit',
    'is ripping us off! We are so weak',
    'is ripping us off',
    'is deeply troubled',
    'is totally corrupt',
    'is killing us',
    'is killing us in every way',
    'has totally killed us',
    'is not our friend',
    '-- what a fool',
    'is corrupt. So corrupt, folks',
    'is totally lost',
    'is a total mess',
    'is trying hard to hide from me',
    'is small and unimportant',
    'is inaccurate',
    'looks very strange',
    'is so wrong, so often',
    'might be controlled by China?',
    'is giving away our money to CHINA, folks',
    'is pure scum',
    'is so dishonest',
    'is killing us',
    'is very untalented',
    'is considered by many to be the worst',
    'is incompetent',
    'is poorly run and managed',
    'is worthless',
    'is highly unethical (and boring)',
    'has become very desperate',
    'is in total turmoil',
    'treats me very badly',
    'is losing',
    'has sold us out',
    'is losing to MEXICO and CHINA',
    'is killing us very badly',
    'has lost its way',
    'is so off',
    'has gone off the rails',
    'is a waste of time',
    'only says negative things about me',
    'is such a troublemaker',
    'is a money-losing failure',
    'has no $ and no talent',
    'is not very good or professional',
    'is so biased it is disgusting',
    'has no power',
    'is just plain dumb',
    'can\'t get anything right',
    'is crazy',
    'is so crazy',
    '-- CRAZY! Very crazy, folks',
    'is a waste',
    'is leading America to slaughter',
    'is totally ineffective & has been for years',
    'is such a scam on our country',
    'is very stupid & highly incompetent',
    'is running the U.S.A. into the ground',
    'is nonsense',
    'is phony',
    'is killing us - killing our great nation',
    'is beating us',
    'is beating us BADLY',
    'is beating us like dogs',
    'is a tool of ISIS!!! Many people say that',
    'is very soft! Zero strength',
    'is a disgrace',
    'has a major inferiority complex',
    'is a dopey clown',
    'is weak and a Washington puppet',
    'has no chance',
    'is wrong on so many subjects',
    'should be thrown out',
    'is BORING',
    'is broken down',
    'is so wrong',
    'is bad (and boring)'
]
endings = [
    'SAD',
    'STUPID',
    'WOW',
    'Unbelieveable',
    'Seriously',
    'So sad',
    'Very sad',
    'Can you believe it?',
    'Dummy',
    'What a dope',
    'Shameful',
    'Awful',
    'What a joke',
    'It\'s true!!'
]


def get_tokens():
    app_key = tokens['app_key']
    app_secret = tokens['app_secret']
    oauth_token = tokens['oauth_token']
    oauth_token_secret = tokens['oauth_token_secret']
    return Twython(app_key, app_secret, oauth_token, oauth_token_secret)


def get_page(url_ending):
    url = BASE_URL + url_ending
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml')
    return soup


def get_title(scraped_page):
    title = scraped_page.find(id='firstHeading')
    if title:
        return title.get_text()
    else:
        False


def get_image(scraped_page):
    table = scraped_page.find('table', class_='infobox')
    if table:
        image_thumb = table.find('img')
        if image_thumb and image_thumb.has_attr('data-file-width'):
            if image_size_correct(image_thumb):
                image_thumb_tag = scraped_page.find('a', class_='image')
                if image_thumb_tag:
                    image_url = get_page(image_thumb_tag['href']).find(class_='fullImageLink').find('a')['href']
                    if image_type_correct(image_url):
                        return image_url
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def image_size_correct(image):
    if int(image['data-file-width']) > 300:
        return True
    else:
        return False


def image_type_correct(var):
    if var.lower().endswith(('.png', '.jpg', '.jpeg')):
        return True
    else:
        return False


def save_image(image_url):
    img_name = image_url.split('/')[-1]
    f = open('img/' + img_name, 'wb')
    f.write(requests.get('http:' + image_url).content)
    f.close()
    return 'img/' + img_name


def write_tweet(title):
    if any(char.isdigit() for char in title):
        text = "Does anyone think %s was good? %s!" % (title, random.choice(endings))
        return text
    else:
        text = "The %s %s %s. %s!" % (random.choice(adjectives), title.title(), random.choice(insults), random.choice(endings))
        return text


def has_char_exception(title):
    if any(char in title for char in exceptions):
        return True
    else:
        return False


def post_tweet(text, image):
    twitter = get_tokens()
    image = open(image, 'rb')
    response = twitter.upload_media(media=image)
    twitter.update_status(status=text, media_ids=[response['media_id']])
    print text
    time.sleep(2)


def fits_in_tweet(text):
    chars = len(text)
    if chars > 116:
        return False
    else:
        return True


def main():
    page = get_page(RANDOM)
    title = get_title(page)
    image = get_image(page)
    if title and image:
        if not has_char_exception(title):
            text = write_tweet(title)
            if fits_in_tweet(text):
                image_path = save_image(image)
                post_tweet(text, image_path)
            else:
                main()
        else:
            main()
    else:
        main()


if __name__ == '__main__':
    main()
