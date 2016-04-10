var uglify = require('gulp-uglify'),
    sourcemaps = require('gulp-sourcemaps'),
    gulp = require('gulp');

gulp.task('uglify', function () {
    return gulp.src(['js/**/*.js'])
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('dest/js'));
});

gulp.task('watch', function () {
    gulp.watch('js/**/*.js', ['uglify']);
})