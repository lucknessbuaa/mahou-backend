module.exports = {
    baseUrl: ".",
    paths: {
        // dependencies
        'jquery': 'assets/components/jquery/jquery.min',
        'radiu': 'assets/components/radiu/radiu',
        'jquery.iframe-transport': 'assets/components/jquery.iframe-transport/jquery.iframe-transport',
        'select2': 'assets/components/select2/select2',
        'moment': 'assets/components/moment/moment',
        'jquery.ui.core': 'assets/components/jqueryui/ui/jquery.ui.core',
        'jquery.ui.mouse': 'assets/components/jqueryui/ui/jquery.ui.mouse',
        'jquery.ui.widget': 'assets/components/jqueryui/ui/jquery.ui.widget',
        'jquery.ui.sortable': 'assets/components/jqueryui/ui/jquery.ui.sortable',
        'when': "assets/components/when",
        "backbone": "assets/components/backbone",
        'bootstrap': 'assets/components/bootstrap/dist/js/bootstrap.min',
        'bootstrap-alert': 'assets/components/bootstrap-alert/alert',
        'jquery-placeholder': 'assets/components/jquery-placeholder/jquery.placeholder',
        'jquery.pnotify': 'assets/components/pnotify/jquery.pnotify.min',
        'jquery.cookie': 'assets/components/jquery.cookie/jquery.cookie',
        'jquery.serializeObject': 'assets/components/jQuery.serializeObject/dist/jquery.serializeObject.min',
        'django-csrf-support': 'assets/components/django-csrf-support/index',
        'parsley': 'assets/components/parsleyjs/parsley',
        'underscore': 'assets/components/underscore/underscore',
        'bootstrap-datetimepicker': "assets/components/smalot-bootstrap-datetimepicker/js/bootstrap-datetimepicker.min",
        'zh-CN': "assets/components/smalot-bootstrap-datetimepicker/js/locales/bootstrap-datetimepicker.zh-CN",
        'multiline': 'assets/components/multiline/browser',

        //base modules
        'codes': 'assets/js/codes',
        'errors': 'assets/js/errors',
        'utils': 'assets/js/utils',
        'chart': 'assets/js/ChartNew',
        'modals': 'assets/js/modals',
        'formProto': 'assets/js/formProto',
        'formValidationProto': 'assets/js/formValidationProto',
        'simple-upload': 'assets/js/simple-upload',

        // app modules
        'login': 'base/js/login',
        'magician': 'backend/js/magician',
        'show': 'backend/js/show',
        'new': 'backend/js/new',
    },
    shim: {
        'jquery-placeholder': {
            deps: ['jquery']
        },

        'jquery.ui.core': {
            deps: ['jquery']
        },
        'jquery.ui.widget': {
            deps: ['jquery', 'jquery.ui.core']
        },
        'jquery.ui.mouse': {
            deps: ['jquery', 'jquery.ui.widget']
        },
        'jquery.ui.sortable': {
            deps: ['jquery', 'jquery.ui.core', 'jquery.ui.mouse', 'jquery.ui.widget']
        },

        'jquery.serializeObject': {
            deps: ['jquery']
        },
        'select2': {
            deps: ['jquery']
        },
        'jquery.iframe-transport': {
            deps: ['jquery']
        },
        'bootstrap': {
            deps: ['jquery']
        },
        'jquery.cookie': {
            deps: ['jquery']
        },
        'parsley': {
            deps: ['jquery']
        }
    }
};
