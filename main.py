from receipe_scrapper import Receipe_scrapper

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
receipe_scp = Receipe_scrapper('chicken')
receipe_scp.collect_receipe()
receipe_scp.close()