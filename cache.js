function DataCache () {
    this.data = {};
}

DataCache.prototype = {
    constructor: DataCache,
    get: function(key) {
        if (this.data.hasOwnProperty(key)) {
            var now = new Date().valueOf() / 1000;
            if (this.data[key].expiration > now) {
                return this.data[key].data;
            }
        }
        return null;
    },
    add: function(key, data, ttl) {
        this.data[key] = {
            expiration: (new Date().valueOf() / 1000) + ttl,
            data: data
        };
    }
};
