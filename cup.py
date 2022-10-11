#################################################################
#water jug problem 
# credit by Phantom
#################################################################
import discord
from discord.ext import commands
# iterate data
# cup max volume
data= list()
cup_max= []
# the data of a combination
class Combination:
    def __init__(self, init_father_index: int, init_step: int, init_status: str, init_list: list):
        self.father_index = init_father_index
        self.step = init_step
        self.status = init_status
        self.cups_volume = init_list
# answer object
ans = Combination(0, 0, '', list())
class Water_jug_problem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        help = 
        '''
            measure the qantity of water without measuring cup><
            step 1: tell me the number of cups(max= 5) ex 3
            step 2: type in the max quantity of each jug respectively ex  5
                                                                          8
                                                                          11
            not 5 8 11 ><
            step 3: tell me the quantity you wanted to get from the above input
            note: it will crash if you type in a non-interger type input
        '''
            ,
        brief = "for fun"
    )
    async def cup(self, ctx):
        global data, cup_max, ans
        # cup count
        vvv= 0
        await ctx.send("stardo><")
        #await ctx.send("please type in the cup num(max= 5): ")
        n = await self.bot.wait_for('message', timeout= 300.0)
        n = int(n.content)
        for i in range(int(n)):
            #await ctx.send("please type in the max quantity of each jug: ")
            z= await self.bot.wait_for('message', timeout= 300.0)
            cup_max.append(int(z.content))
        #await ctx.send("the final quantity of water: ")
        t= await self.bot.wait_for('message', timeout= 300.0)
        t= int(t.content)
        # current pop index
        cur_p = int(0)
        # initialize first combination
        data.append(Combination(0, 0, '', [0] * n))
        # the function for status checking
        # if we find the answer, return True; otherwise, return False
        def check_and_manipulate(father_ind, needed_step, status, detect_comb: list) -> bool:
            global data, ans, cup_max
            # the needed volume is already in the new combination
            if t in detect_comb:
                ans = Combination(father_ind, needed_step, status, new_comb)
                return True
            # the combination is already in the data
            if detect_comb in [cups_data.cups_volume for cups_data in data]:
                return False
            # if two former test failed, that means this is a new combination
            data.append(Combination(father_ind, needed_step, status, new_comb))
            return False
        # main program
        # initialize find status, which is equivalent to 'flag'
        find = bool(False)
        while cur_p < len(data):
            # print(f'Searching... ({cur_p}/{len(data) - 1})')
            # try 1: fill cup to maximum volume
            for cup_index in range(n):
                # if the cup is already full, then skip this step
                if data[cur_p].cups_volume[cup_index] == cup_max[cup_index]:
                    continue
                new_comb = data[cur_p].cups_volume.copy()
                # fill the cup of index 'cup_index' to its maximum volume
                new_comb[cup_index] = cup_max[cup_index]
                find = check_and_manipulate(cur_p, data[cur_p].step + 1, f'Fill cup {cup_index + 1}', new_comb)
                if find:
                    break
            if find:
                break
            # try 2: pour water from cup a to b
            for a_index in range(n):
                for b_index in range(n):
                    # situation 1: if a-cup is b-cup, then skip this step
                    # situation 2: if a-cup is empty, then skip this step
                    # situation 3: if b-cup is full, then skip this step
                    if a_index == b_index \
                            or data[cur_p].cups_volume[a_index] == 0 \
                            or data[cur_p].cups_volume[b_index] == cup_max[b_index]:
                        continue
                    new_comb = data[cur_p].cups_volume.copy()
                    # criterion: delta value <= a-cup
                    # situation 1: if a-cup currently has more water than b_max - b-cup,
                    # then the delta value is b_max - b-cup
                    # situation 2: if a-cup currently has less water than b_max - b-cup,
                    # then the delta value is just a-cup itself
                    delta_volume = min(cup_max[b_index] - new_comb[b_index], new_comb[a_index])
                    new_comb[a_index] -= delta_volume
                    new_comb[b_index] += delta_volume
                    find = check_and_manipulate(
                        cur_p,
                        data[cur_p].step + 1,
                        f'Pour water {delta_volume} from cup {a_index + 1} to {b_index + 1}',
                        new_comb
                    )
                    if find:
                        break
                if find: 
                    break
            if find:
                break
            # try 3: pour the water out of the cup
            for cup_index in range(n):
                # if the cup is empty, then skip this step
                if data[cur_p].cups_volume[cup_index] == 0:
                    continue
                new_comb = data[cur_p].cups_volume.copy()
                # pour the water out of the cup of index 'cup_index'
                new_comb[cup_index] = 0
                find = check_and_manipulate(
                    cur_p,
                    data[cur_p].step + 1,
                    f'Empty cup {cup_index + 1}',
                    new_comb
                )
                if find:
                    break
            if find:
                break
            cur_p += 1
        if not find:
            await ctx.send('不要為難我了qwq, 這是不可能的任務')
        else:
            await ctx.send(f'恭喜！\\^~^ 你只要 {ans.step} 步就可以得到 {t} 的水量！')
            step_list = list()
            step_list.append(f'{ans.cups_volume}, {ans.status}')
            # initialize current father_index to search
            father_index = ans.father_index
            # get the cups_volume data from father_index, and update the next father_index
            while father_index != 0:
                step_list.append(f'{data[father_index].cups_volume}, {data[father_index].status}')
                father_index = data[father_index].father_index
            # because we're searching from back, we'll need to reverse the step logs
            step_list.reverse()
            await ctx.send('以下是步驟！')
            for step in step_list:
                await ctx.send(step)
        cup_max.clear()
        data.clear()
def setup(bot):
    bot.add_cog(Water_jug_problem(bot))