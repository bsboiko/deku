var app = app || {};

app.HandView = Backbone.View.extend({

  el: "#container",

  initialize: function() { 
    _.bindAll(this, "newCard");
    vent.bind("newCard", this.newCard);
    new app.SlidebarView();
    this.collection = new app.Deck();
    this.collection.fetch({reset:true});
    this.render();
    this.listenTo(this.collection, 'add', this.renderCard);
    this.listenTo(this.collection, 'reset', this.render);
  },

  render: function() {
    this.collection.each(function(item) {
      this.renderCard(item);
      }, this);
  },

  renderCard: function(item) {
    var cardView = new app.CardView({
      model: item
    });
    //this is the cards content
    var elem = cardView.render().el;
    this.$el.prepend(elem); //add to the container
    app.msnry.prepended(elem); //add to masonry
    app.msnry.layout();
  },

  newCard: function(card) {
    this.collection.create(card);
  }

});
