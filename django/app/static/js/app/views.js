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
		var html = this.template({friends: this.collection.toJSON() });
		this.$el.empty().append(html);
	}
});

app.MutualPhotosListView = Backbone.View.extend({
	el: '#mutual-photos',
	template: _.template($('#mutual-photos-template').html()),
	collection: new app.MutualPhotosCollection(),

	initialize: function() {
		_.bindAll(this, ['render']);
		this.collection.fetch({ success: this.render });
	},

	render: function() {
		var html = this.template({photos: this.collection.toJSON() });
		this.$el.empty().append(html);
	}
});

app.MutualLikesListView = Backbone.View.extend({
	el: '#mutual-likes',
	template: _.template($('#mutual-likes-template').html()),
	collection: new app.MutualLikesCollection(),

	initialize: function() {
		_.bindAll(this, ['render']);
		this.collection.fetch({ success: this.render });
	},

	render: function() {
		var html = this.template({likes: this.collection.toJSON() });
		this.$el.empty().append(html);
	}
});