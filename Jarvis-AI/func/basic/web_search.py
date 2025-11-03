"""
Web Search Module
Handles web searches using various search engines
"""

import webbrowser
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import urllib.parse


class WebSearcher:
    """
    Class for performing web searches
    """

    def __init__(self):
        """
        Initialize web searcher
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def search_google(self, query: str, open_browser: bool = True) -> bool:
        """
        Search Google

        Args:
            query: Search query
            open_browser: If True, open in browser

        Returns:
            True if successful
        """
        try:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            if open_browser:
                webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error searching Google: {e}")
            return False

    def search_bing(self, query: str, open_browser: bool = True) -> bool:
        """
        Search Bing

        Args:
            query: Search query
            open_browser: If True, open in browser

        Returns:
            True if successful
        """
        try:
            url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
            if open_browser:
                webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error searching Bing: {e}")
            return False

    def search_duckduckgo(self, query: str, open_browser: bool = True) -> bool:
        """
        Search DuckDuckGo

        Args:
            query: Search query
            open_browser: If True, open in browser

        Returns:
            True if successful
        """
        try:
            url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
            if open_browser:
                webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")
            return False

    def search_youtube(self, query: str, open_browser: bool = True) -> bool:
        """
        Search YouTube

        Args:
            query: Search query
            open_browser: If True, open in browser

        Returns:
            True if successful
        """
        try:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            if open_browser:
                webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return False

    def get_search_results(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Get search results without opening browser

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results with title and link
        """
        results = []
        try:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            search_results = soup.find_all('div', class_='g')

            for result in search_results[:num_results]:
                title_elem = result.find('h3')
                link_elem = result.find('a')

                if title_elem and link_elem:
                    title = title_elem.get_text()
                    link = link_elem.get('href')
                    if link and link.startswith('http'):
                        results.append({
                            'title': title,
                            'link': link
                        })

        except Exception as e:
            print(f"Error getting search results: {e}")

        return results

    def search_wikipedia(self, query: str) -> Optional[str]:
        """
        Search Wikipedia and get summary

        Args:
            query: Search query

        Returns:
            Wikipedia summary or None
        """
        try:
            import wikipedia
            summary = wikipedia.summary(query, sentences=3)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Please be more specific. Options: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return "No Wikipedia page found for this query."
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return None


web_searcher = WebSearcher()
