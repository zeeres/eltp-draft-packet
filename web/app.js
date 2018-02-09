var app = angular.module('draftPacketApp', []);

app.controller('draftPacketController', function($scope, $http) {
    $scope.packet = [];
    $scope.loading = true;

    $http.get('packet.json').then(data => {
        $scope.packet = data.data;
        $scope.loading = false;
    });
});
