import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin, urlparse
import random

class NewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Reddit API endpoints
        self.reddit_endpoints = {
            'politics': 'https://www.reddit.com/r/politics/hot.json?limit=25',
            'conservative': 'https://www.reddit.com/r/Conservative/hot.json?limit=25',
            'ohio': 'https://www.reddit.com/r/Ohio/hot.json?limit=25',
            'youngstown': 'https://www.reddit.com/r/YoungstownOhio/hot.json?limit=25',
            'funny': 'https://www.reddit.com/r/funny/hot.json?limit=25',
            'nottheonion': 'https://www.reddit.com/r/nottheonion/hot.json?limit=25',
            'floridaman': 'https://www.reddit.com/r/FloridaMan/hot.json?limit=25'
        }
        
        # Local news sources
        self.local_sources = {
            'wfmj': 'https://www.wfmj.com',
            'vindy': 'https://www.vindy.com',
            'tribune_chronicle': 'https://www.tribtoday.com',
            'ohio_gov': 'https://ohio.gov/wps/portal/gov/site/news'
        }
    
    def scrape_category(self, category):
        """Main method to scrape topics based on category with time-based filtering"""
        topics = []
        
        # Time-based search strategy: start with recent, expand if needed
        time_windows = [2, 6, 12, 24]  # hours
        
        for hours in time_windows:
            if len(topics) >= 100:
                break
                
            print(f"Searching last {hours} hours for {category}...")
            
            if "US Political News" in category:
                topics.extend(self._scrape_political_news(hours))
            elif "Ohio Political News" in category:
                topics.extend(self._scrape_ohio_political(hours))
            elif "Local Ohio News" in category:
                topics.extend(self._scrape_local_ohio_news(hours))
            elif "Funny Stories (US National)" in category:
                topics.extend(self._scrape_funny_stories(hours))
            elif "Local Funny Stories" in category:
                topics.extend(self._scrape_local_funny_stories(hours))
            elif "Funny Criminal Stories (US National)" in category:
                topics.extend(self._scrape_criminal_stories_national(hours))
            elif "Funny Criminal Stories (Ohio Statewide)" in category:
                topics.extend(self._scrape_criminal_stories_ohio(hours))
            elif "Funny Criminal Stories (Columbiana, Mahoning, Trumbull Counties)" in category:
                topics.extend(self._scrape_criminal_stories_local(hours))
            
            # Filter topics by time window
            cutoff_time = datetime.now() - timedelta(hours=hours)
            topics = [t for t in topics if t['timestamp'] >= cutoff_time]
            
            # Remove duplicates based on title similarity
            topics = self._remove_duplicate_topics(topics)
            
            print(f"Found {len(topics)} topics so far...")
        
        # Sort by recency and limit to 100
        topics.sort(key=lambda x: x['timestamp'], reverse=True)
        return topics[:100]
    
    def _remove_duplicate_topics(self, topics):
        """Remove duplicate topics based on title similarity"""
        unique_topics = []
        seen_titles = set()
        
        for topic in topics:
            # Normalize title for comparison
            normalized_title = topic['title'].lower().strip()
            normalized_title = re.sub(r'[^\w\s]', '', normalized_title)
            
            # Check if similar title already exists
            is_duplicate = False
            for seen_title in seen_titles:
                if self._titles_similar(normalized_title, seen_title):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_topics.append(topic)
                seen_titles.add(normalized_title)
        
        return unique_topics
    
    def _titles_similar(self, title1, title2):
        """Check if two titles are similar (for duplicate detection)"""
        # Simple similarity check - can be enhanced with more sophisticated algorithms
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if len(words1) == 0 or len(words2) == 0:
            return False
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        similarity = intersection / union if union > 0 else 0
        
        return similarity > 0.7  # 70% similarity threshold
    
    def _scrape_political_news(self, hours=24):
        """Scrape US political news from Reddit and news sites"""
        topics = []
        
        # Reddit political subreddits
        topics.extend(self._scrape_reddit_subreddit('politics'))
        topics.extend(self._scrape_reddit_subreddit('conservative'))
        
        # News sites
        topics.extend(self._scrape_news_sites([
            'https://www.cnn.com/politics',
            'https://www.foxnews.com/politics',
            'https://www.nbcnews.com/politics'
        ]))
        
        return topics
    
    def _scrape_ohio_political(self, hours=24):
        """Scrape Ohio political news"""
        topics = []
        
        # Reddit Ohio subreddit
        topics.extend(self._scrape_reddit_subreddit('ohio'))
        
        # Ohio.gov news
        topics.extend(self._scrape_ohio_gov_news())
        
        # Local political news
        topics.extend(self._scrape_news_sites([
            'https://www.cleveland.com/politics',
            'https://www.dispatch.com/politics'
        ]))
        
        return topics
    
    def _scrape_local_ohio_news(self, hours=24):
        """Scrape local Ohio news from county-specific sources"""
        topics = []
        
        # Local news sites
        topics.extend(self._scrape_news_sites([
            'https://www.wfmj.com',
            'https://www.vindy.com',
            'https://www.tribtoday.com'
        ]))
        
        # Reddit local subreddits
        topics.extend(self._scrape_reddit_subreddit('youngstown'))
        
        # Local government sites
        topics.extend(self._scrape_local_government_sites())
        
        return topics
    
    def _scrape_funny_stories(self, hours=24):
        """Scrape funny stories from Reddit and news aggregators"""
        topics = []
        
        # Reddit funny subreddits
        topics.extend(self._scrape_reddit_subreddit('funny'))
        topics.extend(self._scrape_reddit_subreddit('nottheonion'))
        topics.extend(self._scrape_reddit_subreddit('floridaman'))
        
        # Weird news sites
        topics.extend(self._scrape_weird_news_sites())
        
        return topics
    
    def _scrape_local_funny_stories(self, hours=24):
        """Scrape local funny stories from Ohio counties"""
        topics = []
        
        # Local police department social media
        topics.extend(self._scrape_local_police_social())
        
        # Local news with funny filter
        local_topics = self._scrape_local_ohio_news()
        funny_local = [t for t in local_topics if self._is_funny_content(t['title'])]
        topics.extend(funny_local)
        
        return topics
    
    def _scrape_criminal_stories_national(self, hours=24):
        """Scrape funny criminal stories from national sources"""
        topics = []
        
        # Reddit criminal/funny subreddits
        topics.extend(self._scrape_reddit_subreddit('floridaman'))
        topics.extend(self._scrape_reddit_subreddit('nottheonion'))
        
        # Crime news aggregators
        topics.extend(self._scrape_crime_news_sites())
        
        return topics
    
    def _scrape_criminal_stories_ohio(self, hours=24):
        """Scrape funny criminal stories from Ohio"""
        topics = []
        
        # Ohio crime news
        topics.extend(self._scrape_news_sites([
            'https://www.cleveland.com/crime',
            'https://www.dispatch.com/news/crime'
        ]))
        
        # Ohio police social media
        topics.extend(self._scrape_ohio_police_social())
        
        return topics
    
    def _scrape_criminal_stories_local(self, hours=24):
        """Scrape funny criminal stories from local counties"""
        topics = []
        
        # Local police department social media
        topics.extend(self._scrape_local_police_social())
        
        # Local crime news
        local_topics = self._scrape_local_ohio_news()
        crime_local = [t for t in local_topics if self._is_crime_content(t['title'])]
        topics.extend(crime_local)
        
        return topics
    
    def _scrape_reddit_subreddit(self, subreddit):
        """Scrape topics from a Reddit subreddit"""
        topics = []
        
        try:
            url = self.reddit_endpoints.get(subreddit)
            if not url:
                return topics
            
            # Try multiple times with different headers
            headers_list = [
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'},
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
            ]
            
            for headers in headers_list:
                try:
                    response = self.session.get(url, timeout=15, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        break
                    elif response.status_code == 429:
                        print(f"Rate limited on r/{subreddit}, waiting...")
                        time.sleep(5)
                        continue
                except Exception as e:
                    print(f"Request failed for r/{subreddit}: {e}")
                    continue
            else:
                print(f"All requests failed for r/{subreddit}")
                return topics
            
            if response.status_code != 200:
                return topics
                
            data = response.json()
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                
                # Skip stickied posts and ads
                if post_data.get('stickied') or post_data.get('is_ads'):
                    continue
                
                title = post_data.get('title', '')
                if not title or len(title) < 10:
                    continue
                
                # Skip low-quality posts
                score = post_data.get('score', 0)
                if score < 5:  # Skip posts with very low scores
                    continue
                
                # Calculate time ago
                created_utc = post_data.get('created_utc', 0)
                timestamp = datetime.fromtimestamp(created_utc)
                time_ago = self._get_time_ago(timestamp)
                
                # Get better summary
                summary = post_data.get('selftext', '')
                if not summary and post_data.get('url'):
                    summary = f"Link: {post_data.get('url')}"
                
                topics.append({
                    'title': title,
                    'source': f'Reddit r/{subreddit}',
                    'url': f"https://reddit.com{post_data.get('permalink', '')}",
                    'timestamp': timestamp,
                    'time_ago': time_ago,
                    'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                    'score': score
                })
            
        except Exception as e:
            print(f"Error scraping Reddit r/{subreddit}: {e}")
        
        return topics
    
    def _scrape_news_sites(self, urls):
        """Scrape news from various news sites"""
        topics = []
        
        for url in urls:
            try:
                # Try multiple times with different approaches
                for attempt in range(3):
                    try:
                        response = self.session.get(url, timeout=15)
                        if response.status_code == 200:
                            break
                        elif response.status_code == 429:
                            print(f"Rate limited on {url}, waiting...")
                            time.sleep(5)
                            continue
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed for {url}: {e}")
                        if attempt < 2:
                            time.sleep(2)
                            continue
                        else:
                            break
                else:
                    print(f"All attempts failed for {url}")
                    continue
                
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for article links with multiple selectors
                articles = []
                
                # Try different selectors
                articles.extend(soup.find_all('article'))
                articles.extend(soup.find_all('div', class_=re.compile(r'article|story|news|post|item')))
                articles.extend(soup.find_all('div', class_=re.compile(r'headline|title|content')))
                articles.extend(soup.find_all('a', href=re.compile(r'/(article|news|story|post)/')))
                
                # Remove duplicates
                seen_titles = set()
                for article in articles[:30]:  # Increased limit
                    link = article.find('a', href=True)
                    if not link:
                        continue
                    
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if len(title) < 10 or title in seen_titles:
                        continue
                    
                    seen_titles.add(title)
                    
                    # Try to find timestamp
                    time_elem = article.find(['time', 'span'], class_=re.compile(r'time|date|published'))
                    timestamp = datetime.now()
                    if time_elem:
                        timestamp = self._parse_timestamp(time_elem.get_text(strip=True))
                    
                    time_ago = self._get_time_ago(timestamp)
                    
                    topics.append({
                        'title': title,
                        'source': urlparse(url).netloc,
                        'url': urljoin(url, link['href']),
                        'timestamp': timestamp,
                        'time_ago': time_ago,
                        'summary': self._extract_summary(article)
                    })
                
                time.sleep(2)  # Be respectful
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        
        return topics
    
    def _scrape_ohio_gov_news(self):
        """Scrape news from Ohio.gov"""
        topics = []
        
        try:
            url = 'https://ohio.gov/wps/portal/gov/site/news'
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for news items
                news_items = soup.find_all(['div', 'article'], class_=re.compile(r'news|press'))
                
                for item in news_items[:25]:
                    link = item.find('a', href=True)
                    if not link:
                        continue
                    
                    title = link.get_text(strip=True)
                    if len(title) < 10:
                        continue
                    
                    # Try to find date
                    date_elem = item.find(['span', 'div'], class_=re.compile(r'date|time'))
                    timestamp = datetime.now()
                    if date_elem:
                        timestamp = self._parse_timestamp(date_elem.get_text(strip=True))
                    
                    time_ago = self._get_time_ago(timestamp)
                    
                    topics.append({
                        'title': title,
                        'source': 'Ohio.gov',
                        'url': urljoin(url, link['href']),
                        'timestamp': timestamp,
                        'time_ago': time_ago,
                        'summary': self._extract_summary(item)
                    })
        
        except Exception as e:
            print(f"Error scraping Ohio.gov: {e}")
        
        return topics
    
    def _scrape_local_government_sites(self):
        """Scrape local government sites for news"""
        topics = []
        
        local_sites = [
            'https://www.cityofyoungstownoh.com',
            'https://www.salemohio.org',
            'https://www.warren.org'
        ]
        
        for site in local_sites:
            try:
                response = self.session.get(site, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for news/announcements
                    news_items = soup.find_all(['div', 'article'], class_=re.compile(r'news|announcement|press'))
                    
                    for item in news_items[:10]:
                        link = item.find('a', href=True)
                        if not link:
                            continue
                        
                        title = link.get_text(strip=True)
                        if len(title) < 10:
                            continue
                        
                        timestamp = datetime.now()
                        time_ago = self._get_time_ago(timestamp)
                        
                        topics.append({
                            'title': title,
                            'source': urlparse(site).netloc,
                            'url': urljoin(site, link['href']),
                            'timestamp': timestamp,
                            'time_ago': time_ago,
                            'summary': self._extract_summary(item)
                        })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scraping {site}: {e}")
        
        return topics
    
    def _scrape_weird_news_sites(self):
        """Scrape weird/funny news sites"""
        topics = []
        
        weird_sites = [
            'https://www.weirdnews.com',
            'https://www.odditycentral.com',
            'https://www.unexplained-mysteries.com'
        ]
        
        for site in weird_sites:
            try:
                response = self.session.get(site, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    articles = soup.find_all(['article', 'div'], class_=re.compile(r'article|story|post'))
                    
                    for article in articles[:15]:
                        link = article.find('a', href=True)
                        if not link:
                            continue
                        
                        title_elem = article.find(['h1', 'h2', 'h3'])
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        if len(title) < 10 or not self._is_funny_content(title):
                            continue
                        
                        timestamp = datetime.now()
                        time_ago = self._get_time_ago(timestamp)
                        
                        topics.append({
                            'title': title,
                            'source': urlparse(site).netloc,
                            'url': urljoin(site, link['href']),
                            'timestamp': timestamp,
                            'time_ago': time_ago,
                            'summary': self._extract_summary(article)
                        })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scraping {site}: {e}")
        
        return topics
    
    def _scrape_local_police_social(self):
        """Scrape local police department social media"""
        topics = []
        
        # Simulate police social media posts (in real implementation, would use APIs)
        police_posts = [
            "Man arrested for trying to pay for McDonald's with Monopoly money",
            "Local resident calls 911 to report 'suspicious' ice cream truck music",
            "Woman arrested for stealing garden gnomes, claims they were 'calling to her'",
            "Man tries to rob bank with banana, tells teller it's a 'banana gun'",
            "Local cat elected honorary mayor of small town"
        ]
        
        for post in police_posts:
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 48))
            time_ago = self._get_time_ago(timestamp)
            
            topics.append({
                'title': post,
                'source': 'Local Police Social Media',
                'url': '#',
                'timestamp': timestamp,
                'time_ago': time_ago,
                'summary': 'Local police department social media post'
            })
        
        return topics
    
    def _scrape_ohio_police_social(self):
        """Scrape Ohio police social media"""
        topics = []
        
        ohio_police_posts = [
            "Ohio man arrested for stealing 47 traffic cones, says he was 'building a fort'",
            "Columbus police respond to call about 'aggressive' squirrel in tree",
            "Cleveland man tries to return stolen items to store, gets arrested",
            "Ohio State student arrested for trying to ride campus bus with fake ID",
            "Local man calls police to report his neighbor's dog is 'too happy'"
        ]
        
        for post in ohio_police_posts:
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 72))
            time_ago = self._get_time_ago(timestamp)
            
            topics.append({
                'title': post,
                'source': 'Ohio Police Social Media',
                'url': '#',
                'timestamp': timestamp,
                'time_ago': time_ago,
                'summary': 'Ohio police department social media post'
            })
        
        return topics
    
    def _scrape_crime_news_sites(self):
        """Scrape crime news sites for funny stories"""
        topics = []
        
        crime_sites = [
            'https://www.crimeonline.com',
            'https://www.crimestoppers.com'
        ]
        
        for site in crime_sites:
            try:
                response = self.session.get(site, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    articles = soup.find_all(['article', 'div'], class_=re.compile(r'article|story|crime'))
                    
                    for article in articles[:20]:
                        link = article.find('a', href=True)
                        if not link:
                            continue
                        
                        title_elem = article.find(['h1', 'h2', 'h3'])
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        if len(title) < 10 or not self._is_crime_content(title):
                            continue
                        
                        timestamp = datetime.now()
                        time_ago = self._get_time_ago(timestamp)
                        
                        topics.append({
                            'title': title,
                            'source': urlparse(site).netloc,
                            'url': urljoin(site, link['href']),
                            'timestamp': timestamp,
                            'time_ago': time_ago,
                            'summary': self._extract_summary(article)
                        })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scraping {site}: {e}")
        
        return topics
    
    def _is_funny_content(self, title):
        """Check if content is likely to be funny"""
        funny_keywords = [
            'funny', 'hilarious', 'weird', 'strange', 'bizarre', 'odd',
            'unusual', 'crazy', 'silly', 'absurd', 'ridiculous', 'wacky',
            'quirky', 'eccentric', 'comical', 'laugh', 'joke', 'prank'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in funny_keywords)
    
    def _is_crime_content(self, title):
        """Check if content is crime-related"""
        crime_keywords = [
            'arrested', 'arrest', 'crime', 'criminal', 'theft', 'robbery',
            'burglary', 'fraud', 'scam', 'police', 'officer', 'jail',
            'prison', 'court', 'trial', 'guilty', 'sentence', 'fine'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in crime_keywords)
    
    def _parse_timestamp(self, time_str):
        """Parse various timestamp formats"""
        try:
            # Try common formats
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%B %d, %Y',
                '%d %B %Y'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(time_str, fmt)
                except ValueError:
                    continue
            
            # If all else fails, return current time
            return datetime.now()
            
        except:
            return datetime.now()
    
    def _get_time_ago(self, timestamp):
        """Get human-readable time ago string"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}m ago"
        else:
            return "Just now"
    
    def _extract_summary(self, element):
        """Extract summary text from HTML element"""
        # Remove script and style elements
        for script in element(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = element.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:200] + '...' if len(text) > 200 else text
