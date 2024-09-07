import requests

url = "https://www.nseindia.com/api/ipo-current-issue"

payload = {}
headers = {
  'accept': '*/*',
  'accept-language': 'en-GB,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,gu-IN;q=0.6,gu;q=0.5,en-US;q=0.4',
  'cookie': '_ga=GA1.1.134561553.1724582927; _abck=2845F765B4667AF0A2B5AF15FB387ED8~0~YAAQXoksMWM4wcCRAQAAlL3CxgypERvxnnAdVJp9nD/6ntYRvxCsqSTk16jfecbn1Mj2w+ZLOaO30/7V2d51MHqL29ELp448xmEET4EGfOP39cr/INW97Dd2Ja32nYaDQDjGJvNC6l/1jdoh7+LuSPAL+0kQ5nvRAQ3JW4sNrsPHt5QWR5ggc3pKJHW8FMMakYiWaJ2a9BD3e/g0BywgefqD5pW98D8wF6yuq2g7GrW5mCbBNJ5Usr3QOylyecqTm9eGDBfTxjK7zt2ksBULHRNuxK4vkho+xkcmCXMzsSVlwf7sVaprrbUSkZTBD0OMWG9KO5AYIgIwZDk9K6SY5d0z7sEqSZSCPmwSaXhHUt2/eF33nuFGTlWToFLvGtKyCdde6C+6HNI83HT1AElQUObeCmtam5YqnA==~-1~-1~-1; defaultLang=en; bm_sz=B7D5311BD74C948DCBF349F5EA2D0C9B~YAAQXoksMQBYwcCRAQAAEyvGxhl+Z89BBFV69582beNTGo04JJbvGeaEVFxn/+Sk6AEzy9g7iXRZmbi60blpp6zn8QY5NjTND32OCnxiDHZLUPnFqoD8WqSSKPBry8PBIL1DrkfcYZlu4KUPH0fxeiwcfaANIVfzsm1Bd6Eq3ROIgGy5KQpne1xc2RGdLHvllItMeps36u/gt8Vv4V84D2LskfjnecnEJvwcJbxAXqmyu4TZjiSRrFnSPJhOZfKVT2+5Of+WvaRtXbLCFLsEi5eYMBnQT44Dt63Jh2Lyeo7sb1rlQq6Bm+cdguSz0Yw08+1opsNAqhJs0zOWS+2d3lyrUAc6Iiv/vFNGIbO4+bp3/8doiPEY3R1tmiBcJUwYz7m17IxjvAm+iYdv43uDo3sxUOmzmAmz5ZkUJ6sCkkl7h2yU5b8KVTrnSc9+p/yRomuuDnN+YqC/6klN~4272964~3421508; nsit=bYodGLglmT46b7asKG9rdovC; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcyNTYyODI2OSwiZXhwIjoxNzI1NjM1NDY5fQ.aiEbXh1fdN0yvEEdr3x34fEvK_ddYD0ItuX7vvwj4ek; AKA_A2=A; ak_bmsc=CC1A79DDCC5B7D804207D1C9883786E8~000000000000000000000000000000~YAAQTIksMYi+xLmRAQAApsl1xxmMCQHT5WgIR1x5+NZJyF2As+49FnOvYKnIgiuxZ32lbCb9Jr+a92Uw2Z0qm34F8PMILjMqwecUhA3j7diihGVpWf2ZsdVnsEME/oKN1x30ex/I9zL2vuaB6ISIjw33tCkwuBaMXprbli8YtUHQojC5pVSogQ9erK74sYbBz8QfZSi1KTSyprbvLjyodwbCR8nVKY4KHFq2p/UCM+srTZEhbz2a8enQhObapVWtckPeN38SfegB5pmOCzffkqNoWZX2ruSS2dFeKR0ZmmG7QULjPqjyNUBLcX5VNADnYPEihUMmP+olBfxr4qb4d5AwkkmWQKaOv4HaUjYn8j2gIbhIFJ3h+1yelUrZ2ANVgmKpBdi+q/vZZHytl4Y9NPfXhKYTvuHy9/LKrxl//pFMJXO3RGfNNjruO91Irq3hMYDFqV00ZqtJZBKlmBnZoA==; RT="z=1&dm=nseindia.com&si=cbda6deb-7381-40f0-907a-03e0927f3d75&ss=m0qqilgd&sl=1&se=8c&tt=lq&bcn=%2F%2F684d0d48.akstat.io%2F"; _ga_87M7PJ3R97=GS1.1.1725628270.3.1.1725628381.59.0.0; bm_sv=D13E600C1D3F6829E505BF3A46036F14~YAAQTIksMcbFxLmRAQAAWHl3xxn/5zgN5OWd3eU413+oG7WmWrxqpxrbHZWQwPSys6EmHGYdOIbUsrYSwAM22B0KeE6eZ/5lk30b6WU8rYkANBpw6xmaNvTzXRiV04FkeNmcqEwBBRM+JfB4g3OzH9ksKLcFKchkEcESEogD7JZkKmwR4pkQRhFVdRIxX56HfmdWno9KAtmLsAEtXnTkEYraiFqMJhs4Cbg2y0MbDfLTJ3u1H1cIyWhaEU3Zk6C8CKeF~1; _abck=2845F765B4667AF0A2B5AF15FB387ED8~-1~YAAQToksMYt1mcCRAQAA3Ah6xwwA+FNe1yM5YC+JXlZq1ulFCH6E/t8Oel0pNxgftzpyFDypl5/2mJzkESpV892tbnw5afpwmDRPBPSLTI2309R3sn8Me2SSMc7BMGwKa+/azQdUk7Xo28VDHLynWShrDyiWw1D3NYHC6hmptSFy053QViiVgsKlj8gtJboZ4Go+hdHA3mXI2/WhVCa0HL4q9hPhxQ3K7PML90SliEhwnN95CPMADzv3iaIM9vuqb7RyfNoHNsZsZL8a/8J5bUaGWlLscjWe4q2D50uztpmCa739S0vNAiZhGVIrmIsFJ4Wabpm6KV8w1Qqzcpev5XrAvTc7YLiSiU1sQY0c57XDtBdt5b1n75mXgDqdHCzMKEru0FOgx7WV2EYYgjjv10q+/UPIx54axA==~0~-1~-1; bm_sv=D13E600C1D3F6829E505BF3A46036F14~YAAQToksMYx1mcCRAQAA3Ah6xxnG0khIr/yIhfBzumT49bPIVWCbc2bp2sQO2QQPyv/qWaSg2PoQ2itSQKCFSjUmTTLYArHcWsMNDH+rkUz4Z2xm1AYlxgfN5scKVcZbZQsWwpz5kD0CZEIsllBkO36weEI3I3HfiZUFcr0tenswZTtWO3zfRt4N7VoLqtZ46NsE8bjwTS9HRCMyj/qg3+fz+1mZ03d/PoMzugAebaBRxKXBjYf9sMIX7Y7Q6JuqnWkg~1',
  'priority': 'u=1, i',
  'referer': 'https://www.nseindia.com/market-data/all-upcoming-issues-ipo',
  'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
