from sportsreference.ncaaf.teams import Teams


class Tree():
    def __init__(self, team):
        self.losses = []
        self.tree = {}
        self.total = []

    def add_loss(self, team):
        self.losses.append(team)

    def get_tree(self, team_losses):
        for team in self.losses:
            if team not in self.total:
                self.total.append(team)
                self.tree[team] = self.get_subtree(team, team_losses)



    def get_subtree(self, team, team_losses):
        ''' Return a subtree of losses '''
        sub_tree = {}
        for loss_team in team_losses[team]:
            if loss_team not in self.total:
                self.total.append(loss_team)
                sub = self.get_subtree(loss_team, team_losses)
                sub_tree[loss_team] = sub

        return sub_tree

    def print_tree(self):
        formatData(self.tree, 0)

    def length(self):
        ''' Retrun Tree size '''
        return len(self.total)


def formatData(t,s):
    if not isinstance(t,dict) and not isinstance(t,list):
        print "\t"*s+str(t)
    else:
        for key in t:
            print "\t"*s+str(key)
            if not isinstance(t,list):
                formatData(t[key],s+1)

def get_rankings():
    team_trees = {}
    team_losses = {}
    teams = Teams(2019)
    for team in teams:
	team_losses[team.abbreviation.lower()] = []
	for game in team.schedule:
	    if game.result == "Loss":
		team_losses[team.abbreviation.lower()].append(game.opponent_abbr)

    for team, losses in team_losses.items():
	tree = Tree(team)
	for loss in losses:
	    tree.add_loss(loss)

	team_trees[team] = tree



    rankings = []
    for team, tree in team_trees.items():
	try:
	    tree.get_tree(team_losses)
	    # print "{} tree length: {}".format(team, tree.length())
	    rankings.append((team, tree.length()))
	except:
            pass
	    # print "{} lost to and FCS School".format(team)
	    #print team_losses[team]
    
    rankings.sort(key=lambda x: x[1])

    real_rank = []
    count = 0
    rank = 1
    curr_loss = 0
    for team, losses in rankings:
	count += 1
	if curr_loss != losses:
	    rank = count
	    curr_loss = losses
	rank_tuple = (rank, team.replace("-"," ").title(), losses)
        real_rank.append(rank_tuple)
        
    return real_rank


