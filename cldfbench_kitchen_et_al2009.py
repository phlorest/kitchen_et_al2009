import pathlib

import nexus
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
        
        summary = self.raw_dir.read_tree(
            'kitchen2009.mcct.trees', detranslate=True,
            preprocessor=fix_trees)
        args.writer.add_summary(summary, self.metadata, args.log)

        posterior = self.raw_dir.read_trees(
            'Semitic.Greenhill.trees.gz',
            burnin=200, sample=1000, detranslate=True,
            preprocessor=fix_trees)
        args.writer.add_posterior(posterior, self.metadata, args.log)

        # create nexus file from multistate nexus because we then know the 
        # character labels / word mappings.
        args.writer.add_data(
            self.raw_dir.read_nexus('Kitchen-Semitic-Multistate.nex', preprocessor=fix_nexus),
            self.characters,
            args.log,
            binarise=True)
 
