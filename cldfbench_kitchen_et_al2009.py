import pathlib

import nexus
from nexus.tools.binarise import binarise
import phlorest


def fix_trees(p):
    if not isinstance(p, str):
        p = p.read_text(encoding='utf8')
    return p.replace('.Arabic', '_Arabic')


def fix_nexus(p):
    if not isinstance(p, str):
        p = p.read_text(encoding='utf8')
    return p.replace('Arabic', '_Arabic')  # yes, as above but no full stop


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "kitchen_et_al2009"

    def cmd_makecldf(self, args):
        self.init(args)
        args.writer.add_summary(
            self.raw_dir.read_tree(
                'kitchen2009.mcct.trees', detranslate=True, preprocessor=fix_trees),
            self.metadata,
            args.log)
        
        posterior = self.sample(
            self.remove_burnin(
                fix_trees(self.raw_dir.read('Semitic.Greenhill.trees.gz')),
                200),
            detranslate=True,
            as_nexus=True)

        args.writer.add_posterior(
            posterior.trees.trees,
            self.metadata,
            args.log)
        
        # create nexus file from multistate nexus because we then know the 
        # character labels / word mappings.
        nex = self.raw_dir.read_nexus('Kitchen-Semitic-Multistate.nex',
            preprocessor=fix_nexus)
        nex = binarise(nex)
        nex = nexus.NexusReader.from_string(nex.write(charblock=True))
        args.writer.add_data(nex, self.characters, args.log)
            
            
            