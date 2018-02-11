var app = angular.module('draftPacketApp', []);

$(document).ready(function() {
    $('[data-toggle=tooltip]').tooltip({trigger: 'hover'});

    $('.dropdown-menu:not(.close-on-click)').click(function(e) {
        e.stopPropagation();
    });
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
    $scope.highlights = JSON.parse(localStorage.getItem('highlights') || '{}');

    $scope.countries = [];
    $scope.countryNames = {};

    $scope.filter = {
        countries: {'': true},
        positions: {
            'o': true,
            'o?': true,
            '?': true,
            'd?': true,
            'd': true
        },
        rating: {
            9: true,
            8: true,
            7: true,
            6: true,
            5: true,
            4: true,
            3: true,
            2: true,
            1: true,
            0: true
        },
        highlight: {
            red: true,
            yellow: true,
            green: true,
            blue: true,
            strikethrough: true,
            '': true
        }
    };

    $scope.hasFilter = {
        any: false,
        countries: false,
        positions: false,
        rating: false,
        highlight: false
    };

    $scope.selectX = function(o, v) {
        for(var k in o)
            o[k] = v;
        $scope.updateFilterDisplays();
    };

    $scope.updateFilterDisplays = function() {
        function check(o) {
            for(var k in o)
                if(!o[k])
                    return true;
            return false;
        }
        $scope.hasFilter.countries = check($scope.filter.countries);
        $scope.hasFilter.positions = check($scope.filter.positions);
        $scope.hasFilter.rating = check($scope.filter.rating);
        $scope.hasFilter.highlight = check($scope.filter.highlight);

        $scope.hasFilter.any = $scope.hasFilter.countries
                            || $scope.hasFilter.positions
                            || $scope.hasFilter.rating
                            || $scope.hasFilter.highlight;
    };

    $scope.resetFilters = function() {
        function reset(o) {
            for(var k in o)
                o[k] = true;
        }
        reset($scope.filter.countries);
        reset($scope.filter.positions);
        reset($scope.filter.rating);
        reset($scope.filter.highlight);

        for(var k in $scope.hasFilter)
            $scope.hasFilter[k] = false;
    };

    $scope.matchFilter = function(player) {
        function getPosition(p) {
            if(p.primary !== '?')return p.primary;
            if(p.preference !== '?')return p.preference + '?';
            return p.preference;
        }
        var hl = $scope.highlights[player.profile] || '';
        return $scope.filter.countries[player.country.code]
            && $scope.filter.positions[getPosition(player.position)]
            && $scope.filter.rating[Math.floor(player.rating)]
            && $scope.filter.highlight[hl];
    };

    $scope.setHighlighter = function(h) {
        if($scope.highlighter === h)
            $scope.highlighter = '';
        else
            $scope.highlighter = h;
    };

    $scope.resetHighlights = function() {
        $scope.highlights = {};
        localStorage.setItem('highlights', JSON.stringify($scope.highlights));
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
        $('#packet-container').popover('hide');

        if($scope.highlighter !== '') {
            var player = $scope.packet[i].profile;

            if($scope.highlighter === 'erase')
                delete $scope.highlights[player];
            else
                $scope.highlights[player] = $scope.highlighter;

            localStorage.setItem('highlights', JSON.stringify($scope.highlights));
            return;
        }

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

        var countryCounts = {};
        
        for(var row of data.data) {
            var c = row.country.code;

            if(c === '')
                continue;

            if(!(c in countryCounts))
                countryCounts[c] = 1;
            else
                countryCounts[c]++;

            $scope.countryNames[c] = row.country.name;
            $scope.filter.countries[c] = true;
        }

        $scope.countries = Object.keys(countryCounts).sort((x, y) => countryCounts[y] - countryCounts[x]);

        $scope.loading = false;

        $('#packet-container').popover({
            'placement': 'right',
            'content': 'Click a player to view more information!',
            'trigger': 'manual',
            'offset': '0px 20px'
        }).popover('show');
    });


    $scope.ex_filter = true;
    $scope.ex_columns = [
        {name: 'highlight', title: 'Highlight', active: false, f: player => $scope.highlights[player.profile] || ''},
        {name: 'name', title: 'Name', active: true, f: player => player.name},
        {name: 'profile', title: 'Profile Link', active: false, f: player => 'http://tagpro-chord.koalabeast.com/profile/' + player.profile},
        {name: 'reddit', title: 'Reddit', active: true, f: player => player.reddit},
        {name: 'position', title: 'Position', active: true, f: player => $scope.format_position(player.position)},
        {name: 'rating', title: 'Rating', active: true, f: player => player.rating},
        {name: 'country', title: 'Country', active: false, f: player => player.country.name},
        {name: 'chord', title: 'Chord Ping', active: false, f: player => player.ping.chord},
        {name: 'orbit', title: 'Orbit Ping', active: false, f: player => player.ping.orbit},
        {name: 'microphone', title: 'Microphone', active: true, f: player => player.microphone ? 'Yes' : 'No'},
        {name: 'availability_comment', title: 'Availability Comment', active: true, f: player => player.availability.comment},
        {name: 'extra_information', title: 'Extra Information', active: true, f: player => player.comment},
        {name: 'comment', title: 'Rating Comment', active: false, f: player => player.rating_comment || ''},
        {name: 'winrate_current', title: 'Current Win Rate', active: false, f: player => player.stats.rolling.current},
        {name: 'winrate_best', title: 'Best Win Rate', active: false, f: player => player.stats.rolling.best},
    ];
    $scope.ex_formats = [
        {ext: 'csv', title: 'Comma-separated values (csv)', sep: ','},
        {ext: 'tsv', title: 'Tab-separated values (tsv)', sep: '\t'}
    ];

    $scope.ex_format = 0;

    $scope.ex_selectX = function(v) {
        for(var x of $scope.ex_columns)
            x.active = v;
    };
    $scope.ex_setFormat = function(x) {
        $scope.ex_format = x;
    };

    $scope.download = function() {
        var fmt = $scope.ex_formats[$scope.ex_format];
        var data = '';

        var cols = $scope.ex_columns.filter(c => c.active),
            rows = $scope.ex_filter
                ? $scope.packet.filter($scope.matchFilter)
                : $scope.packet;

        function formatCell(x) {
            if(typeof(x) !== 'string')
                return '' + x;
            x = x.replace(/"/g, '\\"');
            if(x.indexOf(fmt.ext) !== -1)
                return '"' + x + '"';
            return x;
        }

        data += cols.map(c => c.name).map(formatCell).join(fmt.sep) + '\n';
        for(var row of rows) {
            var r = [];
            for(var c of cols)
                r.push(c.f(row));
            data += r.map(formatCell).join(fmt.sep) + '\n';
        }

        // Download it!
        var el = document.createElement('a');
        el.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data));
        el.setAttribute('download', 'packet.' + fmt.ext);
        el.style.display = 'none';
        document.body.appendChild(el);
        el.click();
        document.body.removeChild(el);
    }
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
