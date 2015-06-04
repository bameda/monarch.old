var gulp = require("gulp");

var plumber = require("gulp-plumber");
var cache = require("gulp-cached");
var concat = require("gulp-concat");

var sass = require("gulp-sass");
var sourcemaps = require('gulp-sourcemaps');
var webserver = require("gulp-webserver");


/////////////////////////
// CONS & CONFIGURATION
/////////////////////////
var BOWER_DIR = "./bower_components"
var SRC_DIR = "./monarch/front"
var STATIC_DIR = SRC_DIR + "/static"

var config = {
    bower: {
        boostrapDir: BOWER_DIR + "/bootstrap-sass"
    },
    src: {
        stylesDir: SRC_DIR + "/styles",
        stylesMainFile: SRC_DIR + "/styles/main.scss"
    },
    static: {
        jsDir: STATIC_DIR + "/scripts",
        stylesDir: STATIC_DIR + "/styles",
        fontsDir: STATIC_DIR + "/fonts",
        imagesDir: STATIC_DIR + "/img"
    }
}


/*************************************************************************
 * FONTS
 *************************************************************************/
gulp.task("_fonts", function() {
    return gulp.src(config.bower.boostrapDir + "/assets/fonts/**/*")
               .pipe(gulp.dest(config.static.fontsDir));
});


/*************************************************************************
 * CSS
 *************************************************************************/
gulp.task("_css", function() {
    return gulp.src(config.src.stylesMainFile)
               .pipe(sourcemaps.init())
               .pipe(sass({ includePaths: [
                   config.bower.boostrapDir + "/assets/stylesheets"
                ]}).on('error', sass.logError))
               .pipe(sourcemaps.write({debug: false}))
               .pipe(gulp.dest(config.static.stylesDir));
});


/*************************************************************************
 * WATCH
 *************************************************************************/
gulp.task("watch", function () {
    return gulp.watch(config.src.stylesDir, ["_css"]);
});

gulp.task("server", function () {
    return gulp.src(SRC_DIR)
               .pipe(webserver({
                        livereload: true,
                        port: 8080
                     }))
});

/*************************************************************************
 * MAIN TASKS
 *************************************************************************/
var compiledTasks = ["_fonts",
                     "_css"]

gulp.task("default", compiledTasks.concat(["server",
                                           "watch"]));

gulp.task("deploy", compiledTasks);
