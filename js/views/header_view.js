var app = app || {};

app.HeaderView = Backbone.View.extend({
    el: ".navbar-form",

    template: _.template( $('#login_header').html() ),

    initialize: function() {
        this.listenTo(app.user, "change", this.alertToChange);
        this.render();
    },

    render: function() {
        //for debugging and trials user is a person's default name. Just modified this to reflect that.
        if (app.user.get("firstName") !== "" && app.user.get("firstName") !== "User") {
            this.template = _.template( $('#logout_header').html() );
            this.$el.html(this.template(app.user.toJSON()));
        } else {
            this.template = _.template( $('#login_header').html() );
            this.$el.html(this.template);
        }
    },

    alertToChange: function() {
        console.log("The user's name has changed to " + app.user.get("firstName"));
    }

})
