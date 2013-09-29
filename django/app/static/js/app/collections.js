app.FriendsCollection = Backbone.Collection.extend({
    url: '/facebook/api/friend/',
    model: app.FriendModel
});

app.MutualFriendsCollection = Backbone.Collection.extend({
    model: app.FriendModel,
    url: function() {
        return '/facebook/api/friend/mutual/'+ app.friend.uid +'/';
    }
});

app.MutualPhotosCollection = Backbone.Collection.extend({
    model: app.MutualPhotosModel,
    url: function() {
        return '/facebook/api/photo/with/'+ app.friend.uid +'/';
    }
});

app.MutualLikesCollection = Backbone.Collection.extend({
    model: app.MutualPhotosModel,
    url: function() {
        return '/facebook/api/like/with/'+ app.friend.uid +'/';
    }
});

app.PostsFromMeInFriendTimeline = Backbone.Collection.extend({
    model: app.MutualPostsModel,
    url: function() {
        return '/facebook/api/post/from/me/in_timeline/'+ app.friend.uid +'/';
    }
});

app.PostsFromFriendInMyTimeline = Backbone.Collection.extend({
    model: app.MutualPostsModel,
    url: function() {
        return '/facebook/api/post/from/'+ app.friend.uid +'/in_timeline/me/';
    }
});

app.PostsFromMeTaggedByFriend = Backbone.Collection.extend({
    model: app.MutualPostsModel,
    url: function() {
        return '/facebook/api/post/from/me/tagged/'+ app.friend.uid +'/';
    }
});

app.PostsFromFriendTaggingMe = Backbone.Collection.extend({
    model: app.MutualPostsModel,
    url: function() {
        return '/facebook/api/post/from/'+ app.friend.uid +'/tagged/me/';
    }
});
