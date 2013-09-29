app.FriendListView = Backbone.View.extend({
	el: '#frinds-list',
	template: _.template($('#friends-list-template').html()),
	collection: new app.FriendsCollection(),

	initialize: function() {
		_.bindAll(this, ['render']);
		this.collection.fetch({ success: this.render });
	},

	render: function() {
		var html = this.template({friends: this.collection.toJSON() });
		this.$el.empty().append(html);
	}
});

app.MutualFriendListView = Backbone.View.extend({
	el: '#mutual-friends-list',
	template: _.template($('#mutual-friends-list-template').html()),
	collection: new app.MutualFriendsCollection(),

	initialize: function() {
		_.bindAll(this, ['render']);
	},

	render: function() {
		var that = this, html;
		this.collection.fetch({ success: function(){
			that.collection.trigger('change');
			html = that.template({friends: that.collection.toJSON() });
			that.$el.empty().append(html);
		}});
	}
});

app.MutualPhotosListView = Backbone.View.extend({
	el: '#mutual-photos',
	template: _.template($('#mutual-photos-template').html()),
	collection: new app.MutualPhotosCollection(),

	initialize: function() {
		_.bindAll(this, ['render']);
	},

	render: function() {
		var that = this, html;
		this.collection.fetch({ success: function(){
			that.collection.trigger('change');
			html = that.template({photos: that.collection.toJSON() });
			that.$el.empty().append(html);
		}});
	},
});

app.MutualLikesListView = Backbone.View.extend({
	el: '#mutual-likes',
	template: _.template($('#mutual-likes-template').html()),
	collection: new app.MutualLikesCollection(),

	initialize: function() {
		_.bindAll(this, ['render']);
	},

	render: function() {
		var that = this, html;
		this.collection.fetch({ success: function(){
			that.collection.trigger('change');
			html = that.template({likes: that.collection.toJSON() });
			that.$el.empty().append(html);
		}});
	}
});


app.AppView = Backbone.View.extend({
	el: '#app',

	events: {
		'click .ex-info a' : 'showFriendsList',
		'click .modal-find-ex button' : 'chooseFriend'
	},

	initialize: function() {
		var that = this;
		this.friendsList = new app.FriendListView();
		this.mutualFriendsList = new app.MutualFriendListView();
		this.mutualPhotosList = new app.MutualPhotosListView();
		this.mutualLikesList = new app.MutualLikesListView();
		this.friend = null;

		this.mutualFriendsList.collection.on('change', function() {
			$('.common-friends .count').text(this.length);
		});

		this.mutualPhotosList.collection.on('change', function() {
			$('.common-photos .count').text(this.length);
		});

		this.mutualLikesList.collection.on('change', function() {
			$('.common-likes .count').text(this.length);
		});
	},

	render: function() {
		this.mutualFriendsList.render();
		this.mutualPhotosList.render();
		this.mutualLikesList.render();
	},

	showFriendsList: function( event ) {
		event.preventDefault();
		$('body').addClass('show-modal-ex');
	},

	chooseFriend: function() {
		var id = $('#frinds-list').find('input[name="friend"]:checked').val();
		this.friend = this.friendsList.collection.get(id);
		app.friendId = id;
		$('body').removeClass('show-modal-ex');
		this.updateFriendDetail(this.friend);
	},

	updateFriendDetail: function(friend) {
		if ( friend ) {
			$('.ex-username').text(friend.get('name'));
			$('.ex-search img').attr('src', friend.get('pic_small'));
			this.render();
		}
	}
});