###
# This file is part of the taiga-contrib-fan package.
#
# (c) Simon Leblanc <contact@leblanc-simon.eu>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
# File: fan.coffee
###

template = """
<section class="fan-container" ng-if="projects.length">
    <header><h1 class="title-bar">{{ 'FAVORITE_PROJECTS' | translate }}</h1></header>
    <div class="home-project" ng-repeat="project in projects">
        <div class="project-card-inner" tg-nav="project:project=project.slug">
            <div class="project-card-header">
                <a href="#" tg-nav="project:project=project.slug" class="project-card-logo">
                    <img tg-project-logo-small-src="::project" />
                </a>
                <h3 class="project-card-name">
                    <a href="#" tg-nav="project:project=project.slug">{{ project.name }}</a>
                </h3>
            </div>
            <p class="project-card-description">
                {{ project.description }}
            </p>
        </div>
    </div>
</section>
"""

available_locales = ["fr", "en"]

FanDirective = ($compile, $http, $urls, $translate) ->
    link = ($scope, $el, $attrs) ->
        $http.get($urls.resolve("fan")).then (response) ->
            $scope.projects = response.data
            fanProjects = $compile(template)($scope)
            $el.prepend(fanProjects)
        

    return {link:link}


FanConfig = ($translateProvider) ->
    available_locales.forEach (locale) -> 
        $.get('/plugins/taiga-contrib-fan/taiga-contrib-fan-' + locale + '.json').then (data) ->
            $translateProvider.translations locale, data


FanRun = ($tgUrls) ->
    $tgUrls.update({
        "fan": "/fan"
    })


module = angular.module('taigaContrib.fan', [])

module
    .config(["$translateProvider", FanConfig]) 
    .directive("tgWorkingOn", ["$compile", "$tgHttp", "$tgUrls", "$translate", FanDirective])
    .run(["$tgUrls", FanRun])
