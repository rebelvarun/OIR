analytics = {
        analyticsData: function(code, time, date )
        {
            this.code = code;
            this.timeInfo = new Date().toGMTString();
            this.serverUrl = 'http://localhost/analytics/logdump';
            var data = {code : this.code, time: this.timeInfo, id: this.id};
            sendData(JSON.stringify(data),0, serverUrl);
        },

        clickData: function(code, id, serverUrl){
            this.code = code;
            this.timeInfo = new Date().toGMTString();
            this.id = id;
            var data = {code : this.code, time: this.timeInfo, id: this.id};
            analytics.sendData(JSON.stringify(data),0, serverUrl);
        },
        
        sendData: function(msg, nattempts, sendUrl) {
            var postObj = { data: msg, attempts: nattempts, url: sendUrl};
            $.ajax({
                type: 'POST',
                url: sendUrl,
                data: {data: msg},
                timeout: 6000,
                error: function(jqXHR, textStatus, errorThrown) {
                    if (textStatus == 'timeout') {
                        if (this.attempts <= 5) {
                            sendData(this.data, this.attempts + 1, this.url, this.jqry);
                        }
                    }
                }
            });
        }
};