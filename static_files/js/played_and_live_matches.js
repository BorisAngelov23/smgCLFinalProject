var coll = document.getElementsByClassName("collapsible");
        var i;

        for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                    var matchId = this.getAttribute("data-match-id");
                    loadGoalscorers(content, matchId);
                }
            });
        }

        function loadGoalscorers(content, matchId) {
            var ul = content.querySelector("#goalscorers-" + matchId);

            fetch("/matches/api/match_goalscorers/" + matchId + "/")
                .then(response => response.json())
                .then(data => {
                    ul.innerHTML = '';
                    data.forEach(stats => {
                        if (stats.goals_scored > 0) {
                            var li = document.createElement("li");
                            var a = document.createElement("a");
                            a.href = "/player/" + stats.player_id + "/";
                            a.textContent = stats.player_name + " (" + stats.goals_scored + " goals)";
                            a.style.color = "#0dcaf0";
                            li.appendChild(a);
                            ul.appendChild(li);
                        }
                    });
                    setTimeout(function() {
                        content.style.maxHeight = content.scrollHeight + ul.scrollHeight + "px";
                    }, 100);
                })
                .catch(error => console.error('Error fetching goalscorers:', error));
        }