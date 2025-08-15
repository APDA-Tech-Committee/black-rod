import "bootstrap";

import "../../../node_modules/bootstrap-datepicker/build/build.less"
import "../css/app.scss";

import "bootstrap-datepicker";

import { MDCDataTable } from '@material/data-table';
import { MDCCheckbox } from '@material/checkbox';
import { MDCIconButtonToggle } from '@material/icon-button';
import { MDCMenu } from '@material/menu';
import { MDCTabBar } from '@material/tab-bar';
import { MDCRipple } from '@material/ripple';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(() => {
  $('#expandAll').on('click', function(e) {
    e.preventDefault();
    $('.collapse').toggleClass('show');
  });

  $('.clickable').on('click', function(e) {
    e.preventDefault();
    $($(this).data('newtarget')).toggleClass('show');
  });
  
  $('#create_debater').click((event) => {
    event.preventDefault();

    var to_serialize = $('#debater_create_form').serialize()
    to_serialize = to_serialize + "&first_name=" + $('#id_name').val().split(' ')[0];
    to_serialize = to_serialize + "&last_name=" + $('#id_name').val().split(' ')[1];

    console.log(to_serialize);

    $.post('/core/debaters/create', to_serialize).done((data) => {
      $('#new_debaters').append('<li>' + $('#id_name').val().split(' ')[0] + ' ' + $('#id_name').val().split(' ')[1] + ' (' + $('#select2-id_school-container').html().split('; ')[1] + ') <a href="/core/debaters/' + data + '/delete" class="delete_button">Delete</a>');
      $('#id_name').val('');
      $('#id_school').empty().trigger('change');
      update_delete_listeners();
    });
  });

  $('#id_date').datepicker({
      'format': 'mm/dd/yyyy',
      /* 'startDate': '-3d' */
  });

  $('#teams').on('keyup', team_search);
});

function update_delete_listeners() {
  $('.delete_button').click((event) => {
    event.preventDefault();
    
    $.post($(event.target).attr('href'), {'csrfmiddlewaretoken': getCookie('csrftoken')}).done((data) => {
      $(event.target).parent().remove();
    });
  });
}

function team_search() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('teams');
  filter = input.value.toUpperCase();
  ul = document.getElementById("team_list");
  li = ul.getElementsByTagName('td');
  
  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("button")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

// Initialize Material Design Components
document.addEventListener('DOMContentLoaded', () => {
  // Initialize data tables
  const dataTable = document.querySelector('.mdc-data-table');
  if (dataTable) {
    new MDCDataTable(dataTable);
  }

  // Initialize checkboxes
  const checkboxes = document.querySelectorAll('.mdc-checkbox');
  checkboxes.forEach(checkbox => {
    new MDCCheckbox(checkbox);
  });

  // Initialize icon buttons
  const iconButtons = document.querySelectorAll('.mdc-icon-button');
  iconButtons.forEach(iconButton => {
    new MDCIconButtonToggle(iconButton);
  });
});

document.addEventListener('DOMContentLoaded', () => {
  // Initialize all season menus
  const menuConfigs = [
    { menuId: 'season-menu', buttonId: 'season-button' },
    { menuId: 'soty-season-menu', buttonId: 'soty-season-button' },
    { menuId: 'coty-season-menu', buttonId: 'coty-season-button' },
    { menuId: 'noty-season-menu', buttonId: 'noty-season-button' },
    { menuId: 'online-season-menu', buttonId: 'online-season-button' }
  ];

  menuConfigs.forEach(config => {
    const menuEl = document.getElementById(config.menuId);
    const buttonEl = document.getElementById(config.buttonId);

    if (menuEl && buttonEl) {
      const menu = new MDCMenu(menuEl);
      buttonEl.addEventListener('click', () => {
        menu.open = !menu.open;
      });
    }
  });

  // Initialize tab bar
  const tabBar = document.querySelector('.mdc-tab-bar');
  if (tabBar) {
    new MDCTabBar(tabBar);
  }

  // Initialize all buttons with ripple effect
  const buttons = document.querySelectorAll('.mdc-button');
  buttons.forEach(button => {
    new MDCRipple(button);
  });
});