!function ($) {

  "use strict";


  var Planner = function (element, options) {
    this.$element = $(element);
    this.options = options;
    this.initialize();
  }

  Planner.prototype = {
    initialize: function() {
      this.django_csrf();
      this.row_autoincrement = 1;
      this.bind_menu_events();
      this.bind_refresh();
      this.make_draggable();
      this.autocomplete();
      
      if (localStorage.planner_setup) {
        this.load(JSON.parse(localStorage.planner_setup));
      } else {
        this.add_row(84);
      }
    },

    make_draggable: function() {
      var self = this;

      this.$element.find(".module").draggable({
        snap: ".euro_row, .module",
        snapTolerance: 5,
        containment: "parent",
        start: function(event, ui) {
          self.select_module(this);
        }
      });

      this.$element.find(".euro_row").droppable({
        drop: function(event, ui) {
          $(ui.draggable).attr("data-row", $(this).attr("data-id"));
          self.refresh();
        }
      });
    },

    new_row_id: function() {
      var new_id = this.row_autoincrement;
      this.row_autoincrement += 1;
      return new_id;
    },

    add_row: function(size, row_id) {
      if(typeof(row_id)==='undefined') row_id = this.new_row_id();
      var self = this;

      var info_window = $('<div class="info"></div>').append('<div class="row_data"></div>').append(
        $('<div class="row_nav"></div>').append(
          $('<a href="#"><i class="icon-arrow-up icon-white"></i></a>').on("click", function() {
            self.move_row_up(row_id)
            return false;
          })
        ).append('&nbsp;').append(
          $('<a href="#"><i class="icon-arrow-down icon-white"></i></a>').on("click", function() {
            self.move_row_down(row_id)
            return false;
          })
        ).append('&nbsp;').append(
          $('<a href="#" class="delete_row"><i class="icon-trash icon-white"></i></a>').on("click", function() {
            if (confirm("Are you sure?")) {
              self.delete_row(row_id);
            }
            return false;
          })
        )
      );

      var row = $('<li class="euro_row"></div>')
        .css("width", 10*size)
        .attr("data-size", size)
        .attr("data-id", row_id)
        .append(info_window)
        .prependTo(this.$element.find(".euro_rows"));
      this.make_draggable();
      this.realign_modules();
      this.refresh();
      return row;
    },

    move_row_up: function(row_id) {
      var row = this.$element.find(".euro_row[data-id=" + row_id + "]");
      if (row.prev().length != 0) {
        row.prev().before(row);
        this.realign_modules();
      }
    },

    move_row_down: function(row_id) {
      var row = this.$element.find(".euro_row[data-id=" + row_id + "]");
      if (row.next().length != 0) {
        row.next().after(row);
        this.realign_modules();
      }
    },

    realign_modules: function() {
      var self = this;
      this.$element.find(".euro_row").each(function(index, row) {
        var top = 262 * index;
        self.$element.find(".module[data-row=" + $(row).attr("data-id") + "]").css("top", top);
      });
    },

    delete_row: function(row_id) {
      this.$element.find(".module[data-row=" + row_id + "]").remove();
      this.$element.find(".euro_row[data-id=" + row_id + "]").remove();
      this.refresh();
      this.realign_modules();
    },

    add_module: function(module_id, row_id, local_data) {
      if (typeof(local_data)==='undefined') local_data = false;
      if(typeof(row_id)==='undefined') row_id = this.$element.find(".euro_row").attr("data-id");
      var self = this;

      function insert_module_html(module, left, top) {
        if (typeof(left)==='undefined') left = 0;  
        if (typeof(top)==='undefined') top = 0;

        var inserted_module = $('<div class="module"></div>')
          .addClass("hp" + module.hp)
          .attr({
            "data-row": row_id,
            "data-id": module_id,
            "data-hp": module.hp,
            "data-12v": module.current_12v,
            "data-negative-12v": module.negative_current_12v,
            "data-5v": module.current_5v,
            "data-msrp": module.msrp,
            "data-name": module.name
          })
          .append('<img src="' + module.image + '" alt="' + module.name + '">')
          .css({ left: left, top: top, width: 10*module.hp })
          .appendTo(self.$element.find(".case"));
        self.make_draggable();
        self.bind_module_events(inserted_module)
        self.refresh();
        return inserted_module;
      }

      if (!local_data) {
        $.getJSON("/modules/json/" + module_id, function(data) {
          var module = data.module;
          insert_module_html(module);
        });
      } else {
        var module = new Object();
        module.hp = local_data['size'];
        module.current_12v = local_data['12v'];
        module.current_5v = local_data['5v'];
        module.name = local_data['name'];
        module.image = local_data['image'];
        insert_module_html(module, local_data["left"], local_data["top"]);
      }
    },

    calculate_info: function() {
      var self = this;
      var total_hp = 0, available_hp = 0, total_current_12v = 0, total_negative_current_12v = 0, total_current_5v = 0, total_msrp = 0;
      this.$element.find(".euro_row").each(function(index, element) {
        var hp = 0, current_12v = 0, negative_current_12v = 0, current_5v = 0, msrp = 0;
        self.$element.find(".module[data-row=" + $(element).attr("data-id") + "]").each(function(module_index, module_element) {
          var module_hp = parseInt($(module_element).attr("data-hp"));
          var module_12v = parseInt($(module_element).attr("data-12v"));
          var module_negative_12v = parseInt($(module_element).attr("data-negative-12v"));
          var module_5v = parseInt($(module_element).attr("data-5v"));
          var module_msrp = parseFloat($(module_element).attr("data-msrp"));

          if (!isNaN(module_hp)) hp += module_hp;
          if (!isNaN(module_12v)) current_12v += module_12v;
          if (!isNaN(module_negative_12v)) negative_current_12v += module_negative_12v;
          if (!isNaN(module_5v)) current_5v += module_5v;
          if (!isNaN(module_msrp)) msrp += module_msrp;
        });
        
        var html = "HP: " + hp + "/" + $(element).attr("data-size") + "<br>";
        html += "+12v: " + current_12v + "mA<br>";
        html += "-12v: " + negative_current_12v + "mA<br>";
        html += "5v: " + current_5v + "mA<br>";
        html += "MSRP: $" + msrp;

        $(element).find(".row_data").html(html);

        available_hp += parseInt($(element).attr("data-size"));
        total_hp += hp;
        total_current_12v += current_12v;
        total_negative_current_12v += negative_current_12v;
        total_current_5v += current_5v;
        total_msrp += msrp;
      });

      var total_html = "<h4>Case Totals</h4>";
      total_html += "HP: " + total_hp + "/" + available_hp + "<br>";
      total_html += "+12v: " + total_current_12v + "mA<br>";
      total_html += "-12v: " + total_negative_current_12v + "mA<br>";
      total_html += "5v: " + total_current_5v + "mA<br>";
      total_html += "MSRP: $" + total_msrp;
      this.$element.find(".case_totals").html(total_html);
    },

    save: function() {
      var self = this;
      var save_info = {'version': 1};
      save_info['row_autoincrement'] = this.row_autoincrement;
      save_info['rows'] = [];
      this.$element.find(".euro_row").each(function(index, element) {
        var $element = $(element);
        var modules = [];

        self.$element.find(".module[data-row=" + $element.attr("data-id") + "]").each(function(module_index, module_element) {
          var $module = $(module_element);
          modules.push({
            'id': $module.attr("data-id"),
            'size': $module.attr("data-hp"),
            '12v': $module.attr("data-12v"),
            'negative_12v': $module.attr("data-negative-12v"),
            '5v': $module.attr("data-5v"),
            'msrp': $module.attr("data-msrp"),
            'image': $module.find("img").attr("src"),
            'left': $module.css("left"),
            'top': $module.css("top"),
            'name': $module.attr("data-name")
          });
        });

        var row = {
          'id': $element.attr("data-id"),
          'size': $element.attr("data-size"),
          'modules': modules
        };
        save_info['rows'].push(row);
      });

      return JSON.stringify(save_info);
    },

    save_locally: function() {
      localStorage.planner_setup = this.save();
    },

    save_to_file: function() {
      var preset = this.save();
      this.$element.find(".save_to_file input[name=preset]").val(preset);
      this.$element.find(".save_to_file").submit();
    },

    clear: function() {
      var self = this;
      this.$element.find(".euro_row").each(function(index, element) {
        self.delete_row($(element).attr("data-id"));
      });
    },

    load: function(save_info) {
      var self = this;
      this.row_autoincrement = save_info['row_autoincrement'];
      save_info['rows'].reverse();
      $.each(save_info['rows'], function(index, row) {
        self.add_row(row.size, row.id);
        $.each(row['modules'], function(module_index, module) {
          self.add_module(module.id, row.id, module);
        });
      });
      self.realign_modules();
    },

    bind_menu_events: function() {
      var self = this;

      this.$element.find(".modal .btn_add").on("click", function() {
        $(this).parents(".modal").find("form").submit();
      });

      this.$element.find("#add_row form").on("submit", function() {
        var width = parseInt($(this).find("input[name=width]").val());
        if (!isNaN(width)) self.add_row(width);
        $(this).find("input[name=width]").val("");
        $("#add_row").modal('hide');
        return false;
      });

      this.$element.find("#add_row, #save_online_setup").on("shown", function() {
        $(this).find("input[type=text]").focus();
      });

      this.$element.find("#add_module form").on("submit", function() {
        self.add_module($(this).find("input[name=module_id]").val(), self.$element.find(".euro_row").attr("data-id"));
        $(this).find("input[name=module_id], input[name=autocomplete]").val("");
        $("#add_module").modal('hide');
        return false;
      });

      this.$element.find("#add_module").on("shown", function() {
        $("#add_module input[name=autocomplete]").focus();
      });

      this.$element.find("#add_custom_module form").on("submit", function() {
        self.add_module($(this).find("option:selected").val(), self.$element.find(".euro_row").attr("data-id"));
        $("#add_custom_module").modal('hide');
        return false;
      });

      this.$element.find("#save_online_setup form").on("submit", function() {
        $(this).find("input[name=preset]").val(self.save());
        var name = $(this).find("input[name=name]").val();
        $.post($(this).attr("action"), $(this).serialize(), function(data) {
          var new_option = $("<option></option>").attr("value", data).html(name);
          self.$element.find("#load_online_setup select").append(new_option);
        });

        $("#save_online_setup").modal('hide');
        return false;
      });

      this.$element.find("#load_online_setup form").on("submit", function() {
        $.getJSON("/modules/setup/" + $(this).find("option:selected").val(), function(data) {
          self.clear();
          self.load(JSON.parse(data.setup[0].fields.preset));
          $("#load_online_setup").modal('hide');
        });
        return false;
      });

      this.$element.find("#load_online_setup .btn_delete").on("click", function() {
        if (confirm("Are you sure?")) {
          var $modal = $(this).parents(".modal");
          var setup_id = $modal.find("option:selected").val();
          $.post("/modules/setup/" + setup_id + "/delete/", {}, function(data) {
            $modal.find("option:selected").remove();
          });
        }
        $(this).parents(".modal").modal('hide');
      });

      this.$element.find("#load_from_file input[type=file]").on("change", function(event) {
        var file = event.target.files[0];
        if (file.type == "application/json") {
          var reader = new FileReader();
          reader.onload = (function(theFile) {
            return function(e) {
              self.clear();
              self.load(JSON.parse(e.target.result));
              $("#load_from_file").modal('hide');
            }
          })(file);
          reader.readAsText(file);
          
          self.$element.find("#load_from_file .error").html('');
        } else {
          self.$element.find("#load_from_file .error").html('<div class="alert small">Invalid file type!</div>');
        }

      });

      this.$element.find(".btn_clear").on("click", function() {
        if (confirm("Are you sure?")) {
          self.clear();
        }
      });

      this.$element.find(".btn_delete_selected").on("click", function() {
        self.$element.find(".module.selected").remove();
        self.refresh();
        return false;
      });

      this.$element.find(".btn_save_to_file").on("click", function() {
        self.save_to_file();
      });

      // hack to fix bootstrap dropdown problem
      $('a.dropdown-toggle, .dropdown-menu a').on('touchstart', function(e) {
        e.stopPropagation();
      });
    },

    refresh: function() { this.$element.trigger("refresh") },

    bind_refresh: function() {
      var self = this;
      this.$element.on("refresh", function() {
        self.calculate_info();
        self.save_locally();
      });
    },

    select_module: function(module) {
      var $module = $(module);
      this.$element.find(".module.selected").removeClass("selected");
      $module.addClass("selected");
    },

    deselect_module: function(module) {
      var $module = $(module);
      $module.removeClass("selected");
    },

    bind_module_events: function(module) {
      var self = this;
      $(module).on("click", function() {
        if ($(this).hasClass("selected")) {
          self.deselect_module(module);
        } else {
          self.select_module(module);
        }
      });
    },

    autocomplete: function() {
      var self = this;
      this.$element.find(".module_autocomplete").autocomplete({
        autoFocus: true,
        appendTo: '#add_module form',
        position: {my: "left top", at: "left bottom"},
        source: "/search/autocomplete/",
        select: function(event, ui) {
          self.$element.find("#add_module input[name=module_id]").val(ui.item.id);
        }
      });
    },

    django_csrf: function() {
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      var csrftoken = getCookie('csrftoken');

      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      }
      $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });
    },
  }


 /* PLANNER PLUGIN DEFINITION
  * ========================== */

  $.fn.planner = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('planner')
        , options = $.extend({}, $.fn.planner.defaults, typeof option == 'object' && option)
      if (!data) $this.data('planner', (data = new Planner(this, options)))
    })
  }

  $.fn.planner.defaults = {
    interval: 5000
  , pause: 'hover'
  }

  $.fn.planner.Constructor = Planner
}(window.jQuery);
