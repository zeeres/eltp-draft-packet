var app = angular.module('draftPacketApp', []);

$(document).ready(function() {
    $('[data-toggle=tooltip]').tooltip();
});

app.controller('draftPacketController', function($scope, $http) {
    $scope.packet = [];
    $scope.loading = true;

    $scope.dummy_rows = [];
    for(var i=0; i<50; ++i) $scope.dummy_rows.push(i);

    $scope.selection = -1;
    $scope.player = {};
    $scope.weekly_availability = [];

    $scope.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    $scope.highlighter = '';

    $scope.setHighlighter = function(h) {
        if($scope.highlighter === h)
            $scope.highlighter = '';
        else
            $scope.highlighter = h;

        console.log($scope.highlighter);
    };

    $scope.openToolMenu = function(selector) {
        $('[data-toggle=tooltip]').tooltip('hide');
        $(selector).addClass('open');
    };

    $scope.closeToolMenu = function() {
        $('[data-toggle=tooltip]').tooltip('hide');
        $('.toolmenu.toolmenu-collapsible.open').removeClass('open');
        $scope.highlighter = '';
    };

    $scope.select = function(i) {
        if(i === $scope.selection)
            i = -1;

        $('#packet-container').popover('hide');

        $scope.selection = i;
        if(i >= 0) {
            $scope.player = $scope.packet[i];
            $scope.weekly_availability = $scope.weeksplit($scope.player.availability.weekly);
        }
    };

    $scope.weeksplit = function(w) {
        if(w === undefined)
            return [];
        var l = w.length / 2;
        var out = [];
        for(var i=0; i<l; ++i)
            out.push({first: w[i], second: w[i + l]});
        return out;
    };

    $scope.weeknames = $scope.weeksplit([
        '18-20 Mar',
        '25-27 Mar',
        '1-3 Apr',
        '8-10 Apr',
        '15-17 Apr',
        '22-24 Apr',
        '29-1 Apr',
        '6-8 May',
        '13-15 May',
        '20-22 May',
        '27-29 May',
        '3-5 Jun',
        '10-12 Jun',
        '17-19 Jun'
    ]);

    $scope.format_position = function(pos) {
        if(pos === undefined)
            return '';

        if(pos.primary === 'd')
            return 'Defence only';
        if(pos.primary === 'o')
            return 'Offence only';

        if(pos.preference === 'd')
            return 'Defence preferred';
        if(pos.preference === 'o')
            return 'Offence preferred';

        return 'Doesn\'t matter';
    };

    $http.get('packet.json').then(data => {
        $scope.packet = data.data;
        $scope.loading = false;

        $('#packet-container').popover({
            'placement': 'right',
            'content': 'Click a player to view more information!',
            'trigger': 'manual',
            'offset': '0px 20px'
        }).popover('show');
    });
});

app.directive('availability', function() {
    return {
        'restrict': 'E',
        'scope': {
            'available': '='
        },
        'template': '<span ng-class="[\'fas\', {\'fa-times\': available, \'fa-check\': !available, \'text-danger\': available}]"></span>'
    };
});

app.directive('stars', function() {
    return {
        'restrict': 'E',
        'scope': {
            'rating': '='
        },
        'template': '<span ng-if="rating >= 1" class="fas fa-star"></span>' +
                    '<span ng-if="rating >= 3" class="fas fa-star"></span>' +
                    '<span ng-if="rating >= 5" class="fas fa-star"></span>' +
                    '<span ng-if="rating >= 7" class="fas fa-star"></span>' +
                    '<span ng-if="rating >= 9" class="fas fa-star"></span>' +
                    '<span ng-if="rating > 0 && rating < 1 || rating >= 2 && rating < 3 || rating >= 4 && rating < 5 || rating >= 6 && rating < 7 || rating >= 8 && rating < 9" class="fas fa-star-half"></span>' +
                    '<em ng-if="rating === 0">not rated</em>'
    };
});

app.directive('dailyavailability', function() {
    return {
        'restrict': 'E',
        'scope': {
            'available': '='
        },
        'template': '<span ng-if="available === 0" class="text-danger">Unavailable</span>' +
                    '<span ng-if="available === 1">Available</span>' +
                    '<span ng-if="available === 2" class="text-warning">Would rather not show up</span>' +
                    '<span ng-if="available === 3" class="text-warning">Unsure</span>'
    };
});

// https://gist.github.com/jeffjohnson9046/9470800
app.filter('percentage', ['$filter', function ($filter) {
    return function (input, decimals) {
        return $filter('number')(input * 100, decimals) + '%';
    };
}]);
