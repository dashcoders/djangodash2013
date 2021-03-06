app.FriendListView = Backbone.View.extend({
    el: '#friends-list',
    template: _.template($('#friends-list-template').html()),
    collection: new app.FriendsCollection(),

    initialize: function() {
        _.bindAll(this, ['render']);

        this.$img = $(this.el).siblings('img');

        this.$img.fadeIn();

        this.collection.fetch({ success: this.render });
        $('#search').on('keyup', $.proxy(this.search, this));
    },

    search: function(e) {
        var search, name;

        search = $(e.target).val().toLowerCase().latinize();

        $(this.el).find('li').show();
        $(this.el).find('li').filter(function(index) {
            var name = $(this).data('name').toLowerCase().latinize();

            if(name.indexOf(search) == -1) {
                $(this).hide();
            }
        });
    },

    render: function() {
        this.$img.fadeOut();

        var html = this.template({friends: this.collection.toJSON() });
        this.$el.empty().append(html);
    }
});

app.MutualFriendListView = Backbone.View.extend({
    el: 'div[data-section="mutual-friends"]',
    template: _.template($('#mutual-friends-list-template').html()),
    collection: new app.MutualFriendsCollection(),

    initialize: function() {
        _.bindAll(this, 'render', 'updateCounter');
        this.friendsListEl = $('#mutual-friends-list');
        this.menuButton = $('a[data-section="mutual-friends"]');
        this.counterEl = $('a[data-section="mutual-friends"] .count');
        this.collection.on('change', this.updateCounter);

        $('.reload.friends').on('click', $.proxy(function(e) {
            $(e.target).hide();
            $('.app-content img.loader').fadeIn('fast');
            this.render();
        }, this));
    },

    showLoader: function() {
        this.menuButton.addClass('state-loading');
    },

    hideLoader: function() {
        this.menuButton.removeClass('state-loading');
    },

    hideCounter: function() {
        this.counterEl.fadeTo(300, 0);
    },

    updateCounter: function() {
        this.counterEl.css('opacity', 0).text(this.collection.length).fadeTo(300, 1);
    },

    render: function() {
        var that = this, html;
        this.hideCounter();
        this.showLoader();
        this.collection.fetch({ success: function(){
            that.collection.trigger('change');
            that.hideLoader();
            html = that.template({friends: that.collection.toJSON() });
            that.friendsListEl.empty().append(html);

            $('img.loader').hide();
            $('.reload').fadeIn('fast');
        }});
    }
});

app.MutualPhotosListView = Backbone.View.extend({
    el: 'div[data-section="mutual-photos"]',
    template: _.template($('#mutual-photos-template').html()),
    collection: new app.MutualPhotosCollection(),

    initialize: function() {
        _.bindAll(this, 'render', 'updateCounter');
        this.photosListEl = $('#mutual-photos');
        this.menuButton = $('a[data-section="mutual-photos"]');
        this.counterEl = $('a[data-section="mutual-photos"] .count');
        this.collection.on('change', this.updateCounter);

        $('.reload.photos').on('click', $.proxy(function(e) {
            $(e.target).hide();
            $('.app-content img.loader').fadeIn('fast');
            this.render();
        }, this));
    },

    showLoader: function() {
        this.menuButton.addClass('state-loading');
    },

    hideLoader: function() {
        this.menuButton.removeClass('state-loading');
    },

    hideCounter: function() {
        this.counterEl.fadeTo(300, 0);
    },

    updateCounter: function() {
        this.counterEl.css('opacity', 0).text(this.collection.length).fadeTo(300, 1);
    },

    render: function() {
        var that = this, html;
        this.hideCounter();
        this.showLoader();
        this.collection.fetch({ success: function(){
            that.hideLoader();
            that.collection.trigger('change');
            html = that.template({photos: that.collection.toJSON() });
            that.photosListEl.empty().append(html);

            $('img.loader').hide();
            $('.reload').fadeIn('fast');
        }});
    },
});

app.MutualLikesListView = Backbone.View.extend({
    el: 'div[data-section="mutual-photos"]',
    template: _.template($('#mutual-likes-template').html()),
    collection: new app.MutualLikesCollection(),

    initialize: function() {
        _.bindAll(this, 'render', 'updateCounter');
        this.likesListEl = $('#mutual-likes');
        this.menuButton = $('a[data-section="mutual-likes"]');
        this.counterEl = $('a[data-section="mutual-likes"] .count');
        this.collection.on('change', this.updateCounter);

        $('.reload.likes').on('click', $.proxy(function(e) {
            $(e.target).hide();
            $('.app-content img.loader').fadeIn('fast');
            this.render();
        }, this));
    },

    showLoader: function() {
        this.menuButton.addClass('state-loading');
    },

    hideLoader: function() {
        this.menuButton.removeClass('state-loading');
    },

    hideCounter: function() {
        this.counterEl.fadeTo(300, 0);
    },

    updateCounter: function() {
        this.counterEl.css('opacity', 0).text(this.collection.length).fadeTo(300, 1);
    },

    render: function() {
        $('img.loader').hide();
        $('.reload').fadeIn('fast');

        var that = this, html;
        this.hideCounter();
        this.showLoader();
        this.collection.fetch({ success: function(){
            that.hideLoader();
            that.collection.trigger('change');
            html = that.template({likes: that.collection.toJSON() });
            that.likesListEl.empty().append(html);

            $('img.loader').hide();
            $('.reload').fadeIn('fast');
        }});
    }
});

app.MutualPostListView = Backbone.View.extend({
    el: 'div[data-section="mutual-posts"]',
    template: _.template($('#mutual-posts-template').html()),

    initialize: function() {
        _.bindAll(this, 'render', 'renderSection', 'updateCounter');
        this.menuButton = $('a[data-section="mutual-posts"]');
        this.counterEl = $('a[data-section="mutual-posts"] .count');
        this.postsFromMeInFriendTimeline = new app.PostsFromMeInFriendTimeline();
        this.postsFromFriendInMyTimeline = new app.PostsFromFriendInMyTimeline();
        this.postsFromMeTaggedByFriend = new app.PostsFromMeTaggedByFriend();
        this.postsFromFriendTaggingMe = new app.PostsFromFriendTaggingMe();

        this.postsFromMeInFriendTimeline.on('change', this.updateCounter);
        this.postsFromFriendInMyTimeline.on('change', this.updateCounter);
        this.postsFromMeTaggedByFriend.on('change', this.updateCounter);
        this.postsFromFriendTaggingMe.on('change', this.updateCounter);

        $('.reload.posts').on('click', $.proxy(function(e) {
            $(e.target).hide();
            $('.app-content img.loader').fadeIn('fast');
            this.render();
        }, this));
    },

    showLoader: function() {
        this.menuButton.addClass('state-loading');
    },

    hideLoader: function() {
        this.menuButton.removeClass('state-loading');
    },

    hideCounter: function() {
        this.counterEl.fadeTo(300, 0);
    },

    updateCounter: function() {
        var sum = this.postsFromMeInFriendTimeline.length + this.postsFromFriendInMyTimeline.length + this.postsFromMeTaggedByFriend.length + this.postsFromFriendTaggingMe.length;
        this.counterEl.css('opacity', 0).text(sum).fadeTo(300, 1);
    },

    renderSection: function(sectionTitle, collection, element) {
        var that = this, html;
        this.showLoader();
        collection.fetch({ success: function(){
            that.hideLoader();
            collection.trigger('change');
            html = that.template({ posts: collection.toJSON(), sectionTitle: sectionTitle });
            element.empty().append(html);

            $('img.loader').hide();
            $('.reload').fadeIn('fast');
        }});
    },

    render: function() {
        $('img.loader').hide();
        $('.reload').fadeIn('fast');
        this.hideCounter();
        this.renderSection("My posts in ex's timeline", this.postsFromMeInFriendTimeline, $("#from-me-in-friend"));
        this.renderSection("Ex's posts in my timeline", this.postsFromFriendInMyTimeline, $("#from-friend-in-me"));
        this.renderSection("My posts tagging my ex", this.postsFromMeTaggedByFriend, $("#from-me-tagging-friend"));
        this.renderSection("Ex's posts tagging me", this.postsFromFriendTaggingMe, $("#from-friend-tagging-me"));
    }
});

app.MutualCommentsListView = Backbone.View.extend({
    el: 'div[data-section="mutual-comments"]',
    template: _.template($('#mutual-comments-template').html()),

    events: {
        'click .comment-list a' : 'removeComment'
    },

    initialize: function() {
        _.bindAll(this, 'render', 'renderSection', 'updateCounter');
        this.menuButton = $('a[data-section="mutual-comments"]');
        this.counterEl = $('a[data-section="mutual-comments"] .count');
        this.commentsFromMeInPostsByFriend = new app.CommentsFromMeInPostsByFriend();
        this.commentsFromFriendInPostsByMe = new app.CommentsFromFriendInPostsByMe();

        this.commentsFromMeInPostsByFriend.on('change', this.updateCounter);
        this.commentsFromFriendInPostsByMe.on('change', this.updateCounter);

        $('.reload.comments').on('click', $.proxy(function(e) {
            $(e.target).hide();
            $('.app-content img.loader').fadeIn('fast');
            this.render();
        }, this));
    },

    showLoader: function() {
        this.menuButton.addClass('state-loading');
    },

    hideLoader: function() {
        this.menuButton.removeClass('state-loading');
    },

    hideCounter: function() {
        this.counterEl.fadeTo(300, 0);
    },

    updateCounter: function() {
        var sum = this.commentsFromMeInPostsByFriend.length + this.commentsFromFriendInPostsByMe.length;
        this.counterEl.css('opacity', 0).text(sum).fadeTo(300, 1);
    },

    removeComment: function( event ) {
        event.preventDefault();
        var button = $(event.currentTarget);
        var commentId = button.data('comment-id');
        if ( commentId ) {
            button.addClass('state-loading');
            $.ajax({
                type: 'DELETE',
                url: '/facebook/api/comment/' + commentId + '/',
                success: function() {
                    button.parents('li').fadeOut(function(){
                        $(this).remove();
                    });
                }
            });
        }
    },

    renderSection: function(sectionTitle, collection, element) {
        var that = this, html;
        this.showLoader();
        collection.fetch({ success: function(){
            that.hideLoader();
            collection.trigger('change');
            html = that.template({ comments: collection.toJSON(), sectionTitle: sectionTitle });
            element.empty().append(html);

            $('img.loader').hide();
            $('.reload').fadeIn('fast');
        }});
    },

    render: function() {
        $('img.loader').hide();
        $('.reload').fadeIn('fast');
        this.hideCounter();
        this.renderSection("Comments from me in posts by my ex", this.commentsFromMeInPostsByFriend, $("#comments-from-me"));
        this.renderSection("Comments from my ex's in posts by me", this.commentsFromFriendInPostsByMe, $("#comments-from-friend"));
    }
});

app.AppView = Backbone.View.extend({
    el: '#app',

    events: {
        'click .ex-info a' : 'showFriendsList',
        'click .modal-find-ex button' : 'closeModal',
        'click a[data-section]' : 'showSection',
        'click #friends-list li': 'chooseFriend'
    },

    initialize: function() {
        var that = this;
        this.friendsList = new app.FriendListView();
        this.mutualFriendsList = new app.MutualFriendListView();
        this.mutualPhotosList = new app.MutualPhotosListView();
        this.mutualLikesList = new app.MutualLikesListView();
        this.mutualPostList = new app.MutualPostListView();
        this.mutualCommentsList = new app.MutualCommentsListView();
        this.handleLocalStorage();
    },

    handleLocalStorage: function() {
        var friend = JSON.parse(localStorage.getItem('friend'));
        if ( friend ) {
            app.friend = friend;
            this.updateFriendDetail(friend);
        }
        else {
            $('body').addClass('show-modal-ex');
        }
    },

    render: function() {
        this.hideAllSections();
        this.mutualFriendsList.render();
        this.mutualLikesList.render();
        this.mutualPhotosList.render();
        this.mutualPostList.render();
        this.mutualCommentsList.render();

        this.showFriendSection();
    },

    hideAllSections: function() {
        $('div[data-section]').hide();
    },

    showFriendSection: function() {
        var section = $('div[data-section="mutual-friends"]');

        $('div[data-section]').not(section).hide();
        section.show().scrollTop(0);
    },

    showSection: function( event ) {
        event.preventDefault();
        var section = $('div[data-section="'+ $(event.currentTarget).data('section') +'"]');
        $('div[data-section]').not(section).hide();
        section.show().scrollTop(0);
    },

    showFriendsList: function( event ) {
        event.preventDefault();
        $('body').addClass('show-modal-ex');
    },

    closeModal: function() {
        $('body').removeClass('show-modal-ex');
    },

    chooseFriend: function(e) {
        var $li = $(e.target),
            id;

        $li.find('input').attr('checked', 'checked');

        id = $('#friends-list').find('input[name="friend"]:checked').val();

        app.friend = this.friendsList.collection.get(id).toJSON();
        $('body').removeClass('show-modal-ex');
        this.updateFriendDetail(app.friend);
    },

    updateFriendDetail: function( friend ) {
        if ( friend ) {
            localStorage.setItem('friend', JSON.stringify(friend));
            $('.ex-username').text(friend.name);
            $('.ex-search img').attr('src', friend.pic_small);
            this.render();
        }
    }
});
