!function ($) {

  "use strict";


  var Planner = function (element, options) {
    this.$element = $(element);
    this.options = options;
    this.initialize();
  }

  Planner.prototype = {
    initialize: function() {
      this.row_autoincrement = 1;
      this.bind_menu_events();
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
        containment: "parent",
        start: function(event, ui) {
          self.select_module(this);
          self.$element.find(".module_trash").addClass("active");
        },
        stop: function() {
          self.$element.find(".module_trash").removeClass("active");
        }
      });

      this.$element.find(".euro_row").droppable({
        drop: function(event, ui) {
          $(ui.draggable).attr("data-row", $(this).attr("data-id"));
          self.calculate_info();
        }
      });

      this.$element.find(".module_trash").droppable({
        drop: function(event, ui) {
          $(ui.draggable).remove();
          self.calculate_info();
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
        .appendTo(this.$element.find(".euro_rows"));
      this.make_draggable();
      this.calculate_info();

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
      this.calculate_info();
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
            "data-5v": module.current_5v,
            "data-name": module.name
          })
          .append('<img src="' + module.image + '" alt="' + module.name + '">')
          .css({ left: left, top: top, width: 10*module.hp })
          .appendTo(self.$element.find(".case"));
        self.make_draggable();
        self.bind_module_events(inserted_module)
        self.calculate_info();
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
      this.$element.find(".euro_row").each(function(index, element) {
        var hp = 0, current_12v = 0, current_5v = 0;
        self.$element.find(".module[data-row=" + $(element).attr("data-id") + "]").each(function(module_index, module_element) {
          var module_hp = parseInt($(module_element).attr("data-hp"));
          var module_12v = parseInt($(module_element).attr("data-12v"));
          var module_5v = parseInt($(module_element).attr("data-5v"));

          if (!isNaN(module_hp)) hp += module_hp;
          if (!isNaN(module_12v)) current_12v += module_12v;
          if (!isNaN(module_5v)) current_5v += module_5v;
        });
        
        var html = "HP: " + hp + "/" + $(element).attr("data-size") + "<br>";
        html += "12v: " + current_12v + "mA<br>";
        html += "5v: " + current_5v + "mA<br>";
        $(element).find(".row_data").html(html);
      });
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
            '5v': $module.attr("data-5v"),
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

      $.each(save_info['rows'], function(index, row) {
        self.add_row(row.size, row.id);
        $.each(row['modules'], function(module_index, module) {
          self.add_module(module.id, row.id, module);
        });
      });
    },

    bind_menu_events: function() {
      var self = this;

      function toggle_classes(element, form) {
        $(element).toggleClass("active");
        $(form).toggleClass("active");

        if ($(element).hasClass("active")) {
          $(element).siblings().removeClass("active");
          $(form).siblings().removeClass("active");
        }
      }

      this.$element.find(".btn_add_row").on("click", function() {
        var form = self.$element.find(".add_row");
        toggle_classes(this, form);
        form.find("input[type=text]").focus();
        return false;
      });

      this.$element.find(".btn_add_module").on("click", function() {
        var form = self.$element.find(".add_module");
        toggle_classes(this, form);
        form.find("input[type=text]").focus();
        return false;
      });

      this.$element.find(".btn_load_from_file").on("click", function() {
        var form = self.$element.find(".load_from_file");
        toggle_classes(this, form);
        return false;
      });

      this.$element.find(".add_row").on("submit", function() {
        var width = parseInt($(this).find("input[name=width]").val());
        if (!isNaN(width)) self.add_row(width);
        toggle_classes($(".btn_add_row"), $(this));
        return false;
      });


      this.$element.find(".add_module").on("submit", function() {
        self.add_module($(this).find("input[name=module_id]").val(), self.$element.find(".euro_row").attr("data-id"));
        toggle_classes($(".btn_add_module"), $(this));
        return false;
      });

      this.$element.find(".load_from_file input[type=file]").on("change", function(event) {
        var file = event.target.files[0];
        if (file.type == "application/json") {
          var reader = new FileReader();
          reader.onload = (function(theFile) {
            return function(e) {
              self.clear();
              self.load(JSON.parse(e.target.result));
              toggle_classes(self.$element.find(".btn_load_from_file"), self.$element.find(".load_from_file"));
            }
          })(file);
          reader.readAsText(file);
          
          self.$element.find(".load_from_file .error").html('');
        } else {
          self.$element.find(".load_from_file .error").html('<div class="alert small">Invalid file type!</div>');
        }

      });

      this.$element.find(".btn_clear").on("click", function() {
        if (confirm("Are you sure?")) {
          self.clear();
        }

        $(this).siblings().removeClass("active");
        self.$element.find(".actions form").removeClass("active");
        return false;
      });

      this.$element.find(".btn_save_locally").on("click", function() {
        self.save_locally();
        $(this).siblings().removeClass("active");
        self.$element.find(".actions form").removeClass("active");
      });

      this.$element.find(".btn_save_to_file").on("click", function() {
        self.save_to_file();
        $(this).siblings().removeClass("active");
        self.$element.find(".actions form").removeClass("active");
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
        appendTo: '.add_module',
        position: {my: "left top", at: "left bottom"},
        source: "/search/autocomplete/",
        select: function(event, ui) {
          self.$element.find(".add_module input[name=module_id]").val(ui.item.id);
        }
      });
    }
  }


 /* CAROUSEL PLUGIN DEFINITION
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
