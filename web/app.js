var app = angular.module('draftPacketApp', []);

app.controller('draftPacketController', function($scope, $http) {
    $scope.packet = [];
    $scope.loading = true;

    $scope.selection = -1;
    $scope.player = {};

    $scope.select = function(i) {
        if(i === $scope.selection)
            i = -1;

        $scope.selection = i;
        if(i >= 0)
            $scope.player = $scope.packet[i];
    };

    $scope.format_position = function(pos) {
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
