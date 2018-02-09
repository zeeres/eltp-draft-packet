var app = angular.module('draftPacketApp', []);

app.controller('draftPacketController', function($scope, $http) {
    $scope.packet = [];
    $scope.loading = true;

    $scope.dummy_rows = [];
    for(var i=0; i<50; ++i) $scope.dummy_rows.push(i);

    $scope.selection = -1;
    $scope.player = {};
    $scope.weekly_availability = [];

    $scope.select = function(i) {
        if(i === $scope.selection)
            i = -1;

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
    });
});

app.directive('availability', function() {
    return {
        'restrict': 'E',
        'scope': {
            'available': '='
        },
        'template': '<span ng-class="[\'fas\', {\'fa-times\': available, \'fa-check\': !available, \'unavailable\': available}]"></span>'
    };
});

app.directive('stars', function() {
    return {
        'restrict': 'E',
        'scope': {
            'rating': '='
        },
        'template': '<span class="fas fa-star"></span><span class="fas fa-star"></span><span class="fas fa-star"></span><span class="fas fa-star-half"></span>'
    };
});
