app.FriendItemView = Backbone.View.extend({
	template: _.template($('#friend-item-template').html()),
	model: app.FriendModel
});

app.FriendListView = Backbone.View.extend({

});