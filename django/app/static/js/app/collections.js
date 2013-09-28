app.FriendsCollection = Backbone.Collection.extend({
	url: '/facebook/api/friend/',
	model: app.FriendModel
});