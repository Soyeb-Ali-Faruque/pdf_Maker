angular
   .module('FileManager', ['ui.bootstrap', 'ngFileUpload']);

angular
  .module('FileManager')
  .controller('FileCtrl', FileController)
  ;

  FileController.$inject = ['$scope', 'Upload'];
  function FileController($scope, Upload)
  {
    var vm = this;
    
    vm.progress = 0;
    vm.upload = upload;
    
    function upload(files)
    {
      vm.Files = files;
      
      if (files && files.length)
      {
        Upload.upload({
          url: 'https://angular-file-upload-cors-srv.appspot.com/upload',
          data: {
           files: files
          }
          })
          .then(
          function (response) {
            alert("done");
            // $scope.result = response.data;
           },
          function (response) {
             alert('Error: ' + response.data)
           },
          function (evt) {
            vm.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
            });
        }
    }
  }