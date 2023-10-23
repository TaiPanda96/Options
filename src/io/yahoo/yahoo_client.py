import requests
from requests.exceptions import HTTPError
from pydantic import BaseModel, validator


class YahooHttpInterface(BaseModel):

    """
    Yahoo is a pydantic BaseModel that defines the http connector for yahoo finance.
    """

    url: str = "https://query2.finance.yahoo.com/v7/finance/options/DDOG?formatted=true&crumb=HMQJtZhcT%2FB&lang=en-US&region=US&corsDomain=finance.yahoo.com"
    ticker: str

    @validator("url")
    def validate_url(self, value):
        """
        validate_url validates that the url is non-empty
        """
        if len(value) == 0:
            raise ValueError("URL must be non-empty")
        return value

    def get_by_ticker(self, ticker: str, data_type: str) -> dict:
        """
        get returns financial by ticker from yahoo finance API
        Passing in a ticker and data_type (options, quote, etc.) will return the data for that ticker and data_type
        """
        print(
            "Getting data from yahoo finance API for ticker: "
            + ticker
            + " and data_type: "
            + data_type
        )

        try:
            response = requests.get(
                self.url + ticker + "?formatted=true",
                timeout=3,
                headers=self._headers(),
            )
            if response.status_code == 200:
                return response.json()

            else:
                error = HTTPError(
                    status_code=response.status_code, message=response.reason
                )
                return error

        except HTTPError as e:
            error = HTTPError(status_code=500, message=str(e))
            return error

    def _headers(self) -> dict:
        """
        Static method to return headers for yahoo finance API
        """
        return {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "authority": "query1.finance.yahoo.com",
            "method": "GET",
            "path": "/v7/finance/options/DDOG?formatted=true&crumb=HMQJtZhcT%2FB&lang=en-US&region=US&corsDomain=finance.yahoo.com",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "GUCS=ATibL8kR; GUC=AQEBCAFlNpdlXUIgOASo&s=AQAAALpWmNAv&g=ZTVKWg; A1=d=AQABBIe7p2MCEIPYEq-0c09QGwtRCWrRbJ4FEgEBCAGXNmVdZSUHb2UB_eMBAAcIh7unY2rRbJ4&S=AQAAAnmraLq_jk4S-Ogz63BgdEo; A3=d=AQABBIe7p2MCEIPYEq-0c09QGwtRCWrRbJ4FEgEBCAGXNmVdZSUHb2UB_eMBAAcIh7unY2rRbJ4&S=AQAAAnmraLq_jk4S-Ogz63BgdEo; A1S=d=AQABBIe7p2MCEIPYEq-0c09QGwtRCWrRbJ4FEgEBCAGXNmVdZSUHb2UB_eMBAAcIh7unY2rRbJ4&S=AQAAAnmraLq_jk4S-Ogz63BgdEo; cmp=t=1697991250&j=0&u=1---; gpp=DBAA; gpp_sid=-1; gam_id=y-oi.IcsxE2uJrrJ08d8K6.kM0bJiUzK.Y~A; axids=gam=y-oi.IcsxE2uJrrJ08d8K6.kM0bJiUzK.Y~A&dv360=eS1yNWxranFoRTJ1RWdpZ2RoUV8uaUJDb3owMS4zM2RHQn5B; tbla_id=60fa2283-811f-43b6-9773-94ff6aa9c2b2-tuct7e78543; PRF=t%3DDDOG%26newChartbetateaser%3D0%252C1699204464700",
            "origin": "https://finance.yahoo.com",
            "referer": "https://finance.yahoo.com/quote/DDOG/options?p=DDOG",
            "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        }
