var app = app || {};

app.CreateView = Backbone.View.extend({
  el: '#container',

  events: {
    "submit #create": "getInfo"
  },

  template: "#create-form",

  blurb: "#blurb",

  initialize: function() {
    //listens to the changing of app.user to destroy this view
    this.render();
  },

  render: function() {
    var template = app.TemplateCache.get(this.template),
        blurb = app.TemplateCache.get(this.blurb);
    this.$el.html(blurb).show();
    this.$el.append(template).fadeIn(350);
  },

	formError: function(values) {
		error = false;

		//simple regex for emails. can have upper, lower, -, _, ., and numbers in name
		//and the only hard requirements is .edu
		email_reg = /^\w+([-_.]\w+)*@\w+.edu$/;
    univ_list = $('#university').children().map(function() { return this.value;}).get();

    // a password must be at least eight characters, and must match the confirm password
		if (values.password.length < 8 || values.password !== $('#passwordConfirm').val()) {
			error = true;
			$('#password').val('')
			.attr('placeholder', 'Your password must be at least 8 characters long')
      .focus();
      $('#passwordConfirm').val('')
      .attr('placeholder', 'Confirm your password');
		}
	 
  	if (values.university === '' || $.inArray(values.university, univ_list) === -1) {
	    error = true;
		  $('#univ').val('')
		  .attr('placeholder', 'Please select your university from the list')
      .focus();
	}

		//test if the email is valid
		if (!email_reg.test(values.email)) {
			error = true;
			$('#email').val('')
			.attr('placeholder', 'Enter a valid .edu email address')
      .focus();
		}

		if (values.lastName === '') {
			error = true;
			$('#lastname').val('')
			.attr('placeholder', 'Please enter your last name')
      .focus();
		}

		if (values.firstName === '') {
			error = true;
			$('#firstname').val('')
			.attr('placeholder', 'Please enter your first name')
      .focus();
		}

		return error;
	},

  getInfo: function(event) {
    event.preventDefault();
		//This will make sure the email is unique, and will return the avatar
		var url = "http://localhost:4568/deku/api/users/check_email";

		//this is the data that is sent
		var registerValues = {
			email: $("#email").val(),
			password: $("#password").val().trim(),
			university: $("#univ").val(),
			firstName: $("#firstname").val().trim(),
			lastName: $("#lastname").val().trim()
		};

    var that = this;

		if (!this.formError(registerValues)) {
      /* The user account should not be set up until the end.
       * So for now we are just using app.user to pass the information on
       * to the next view. localStorage is used to validate a logged in user
       * so this will not cause confusion.
       */

      var checkValues = {
        firstName: registerValues.firstName,
        lastName: registerValues.lastName,
        email: registerValues.email
      }
      $.post(url, checkValues, function(data, textStatus, jqXHR) {
        app.user.set(registerValues);
        app.user.set({"avatar": data});
        app.router.navigate('profile', {trigger: true});
      }).fail(function(error) {
        bootbox.alert("That email already exists!");
	  		$('#email').val('')
		  	.attr('placeholder', 'Enter a valid .edu email address')
        .focus();
      });
		}
  }
});
