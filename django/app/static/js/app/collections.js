app.FriendsCollection = Backbone.Collection.extend({
	url: '/facebook/api/friend/',
	model: app.FriendModel
});

app.MutualFriendsCollection = Backbone.Collection.extend({
	model: app.FriendModel
});

app.MutualPhotosCollection = Backbone.Collection.extend({
	model: app.MutualPhotosModel
});

app.MutualLikesCollection = Backbone.Collection.extend({
	model: app.MutualPhotosModel
});