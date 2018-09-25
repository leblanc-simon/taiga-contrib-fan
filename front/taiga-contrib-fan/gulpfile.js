var gulp = require('gulp');
var sass = require('gulp-sass');
var $ = require('gulp-load-plugins')();
var merge = require('merge-stream');

var paths = {
    coffee: 'coffee/*.coffee',
    locales: 'locales/*.json',
    jade: 'partials/*.jade',
    sass: 'sass/*.sass',
    dist: 'dist/'
};

gulp.task('copy-config', function() {
    return gulp.src(['taiga-contrib-fan.json', paths.locales])
        .pipe(gulp.dest(paths.dist));
});

gulp.task('compileJs', function() {
    var jade = gulp.src(paths.jade)
        .pipe($.plumber())
        .pipe($.cached('jade'))
        .pipe($.jade({pretty: true}))
        .pipe($.angularTemplatecache({
            transformUrl: function(url) {
                return '/plugins/taiga-contrib-fan/' + url;
            }
        }))
        .pipe($.remember('jade'));

    var coffee = gulp.src(paths.coffee)
        .pipe($.plumber())
        .pipe($.cached('coffee'))
        .pipe($.coffee())
        .pipe($.remember('coffee'));

    return merge(jade, coffee)
        .pipe($.concat('taiga-contrib-fan.js'))
        //.pipe($.uglify({mangle:false, preserveComments: false}))
        .pipe(gulp.dest(paths.dist));
});

gulp.task('compileCss', function() {
    return gulp.src(paths.sass)
        //.pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        //.pipe(sourcemaps.write())
        .pipe(gulp.dest(paths.dist));
});

gulp.task('watch:js', function() {
    gulp.watch([paths.jade, paths.coffee], ['compileJs']);
});

gulp.task('watch:css', function () {
  gulp.watch(paths.sass, ['compileCss']);
});

gulp.task('default', ['copy-config', 'compileJs', 'compileCss', 'watch:js', 'watch:css']);

gulp.task('build', ['copy-config', 'compileJs', 'compileCss']);
