// app.FriendItemView = Backbone.View.extend({
// 	el: 'li',
// 	template: _.template($('#friend-item-template').html()),
// 	model: app.FriendModel,

// 	initialize: function() {

// 	}
// });

app.FriendListView = Backbone.View.extend({
	el: '#frinds-list',
	template: _.template($('#friends-list-template').html()),
	collection: new app.FriendsCollection(),

	initialize: function() {
		// this.collection.on('fetch', this.render, this);
		_.bindAll(this, ['render']);
		this.collection.fetch({ success: this.render });
	},

	render: function() {
		console.log(this.collection.toJSON());
		var friendsHTML = this.template({friends: this.collection.toJSON() });
		this.$el.empty().append(friendsHTML);
	}
});