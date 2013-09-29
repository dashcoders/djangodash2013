app.FriendsCollection = Backbone.Collection.extend({
    url: '/facebook/api/friend/',
    model: app.FriendModel
});

app.MutualFriendsCollection = Backbone.Collection.extend({
    model: app.FriendModel,
    url: function() {
        return '/facebook/api/friend/mutual/'+ app.friendId +'/';
    }
});

app.MutualPhotosCollection = Backbone.Collection.extend({
    model: app.MutualPhotosModel,
    url: function() {
        return '/facebook/api/photo/with/'+ app.friendId +'/';
    }
});

app.MutualLikesCollection = Backbone.Collection.extend({
    model: app.MutualPhotosModel,
    url: function() {
        return '/facebook/api/like/with/'+ app.friendId +'/';
    }
});